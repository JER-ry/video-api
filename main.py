from cornac.models import BPR
from cornac.data import Dataset
from fastapi import BackgroundTasks, Depends, FastAPI, status
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

bpr = BPR(
    k=10,
    max_iter=100,
    learning_rate=0.001,
    lambda_reg=0.001,
    use_bias=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def train_model():
    data = Dataset.build(crud.db_get_all_watches(Depends(get_db)))
    bpr.fit(data)


@app.get("/check_existence/{user_id}", tags=["user"])
async def check_existence(user_id: str, db: Session = Depends(get_db)):
    return crud.db_check_existence(db, user_id)


@app.put("/register/", status_code=status.HTTP_201_CREATED, tags=["user"])
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.db_register(db, user)


@app.put(
    "/watch/{user_id}/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["player"],
)
async def watch(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_watch(db, user_id, video_id)
    background_tasks.add_task(train_model)


@app.put(
    "/like/{user_id}/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["player"],
)
async def like(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_like(db, user_id, video_id)
    background_tasks.add_task(train_model)


@app.put(
    "/unlike/{user_id}/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["player"],
)
async def unlike(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_unlike(db, user_id, video_id)
    background_tasks.add_task(train_model)


@app.get("/recommend_more/{user_id}", tags=["video_list"])
async def recommend_more(
    user_id: int, old_video_id: set[int], db: Session = Depends(get_db)
):
    recommended_video_id = sorted(
        crud.db_get_some_new_videos(db, user_id, old_video_id),
        key=lambda video_id: bpr.score(user_id, video_id),
    )
    return 0
