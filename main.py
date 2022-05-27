from cornac.data import Dataset
from cornac.models import BPR
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
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/train_model/", tags=["dev"])
def train_model(db: Session = Depends(get_db)):
    bpr.fit(Dataset.build(crud.db_get_all_watches(db)))


# train_model()


@app.get("/check_user_existence/{user_id}", tags=["user"])
def check_user_existence(user_id: str, db: Session = Depends(get_db)):
    return crud.db_check_user_existence(db, user_id)


@app.post("/register/", status_code=status.HTTP_201_CREATED, tags=["user"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.db_register(db, user)


@app.put(
    "/watch/{user_id}/{video_id}",
    tags=["player"],
)
def watch(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_watch(db, user_id, video_id)
    background_tasks.add_task(train_model, db)


@app.put(
    "/like/{user_id}/{video_id}",
    tags=["player"],
)
def like(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_like(db, user_id, video_id)
    background_tasks.add_task(train_model, db)


@app.put(
    "/unlike/{user_id}/{video_id}",
    tags=["player"],
)
def unlike(
    user_id: int,
    video_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    crud.db_unlike(db, user_id, video_id)
    background_tasks.add_task(train_model, db)


@app.get("/recommend_more/{user_id}", tags=["video_list"])
def recommend_more(
    user_id: int,
    old_video_id: set[int],
    final_number_of_videos=6,
    db: Session = Depends(get_db),
):
    user_watched_any = crud.db_user_watched_any(db, user_id)
    if user_watched_any:
        videos = sorted(
            crud.db_get_some_new_videos(db, user_id, old_video_id),
            key=lambda video_id: bpr.score(user_id, video_id),
            reverse=True,
        )[:final_number_of_videos]
    else:
        videos = crud.db_get_some_new_videos(db, user_id, old_video_id)[
            :final_number_of_videos
        ]  # TODO: consider user's interested categories
    return {
        "videos": videos,
        "recommended": user_watched_any,
    }


@app.get("/check_video_existence/{video_id}", tags=["videos"])
def check_video_existence(video_id: int, db: Session = Depends(get_db)):
    return crud.db_check_video_existence(db, video_id)


@app.post("/add_video/", status_code=status.HTTP_201_CREATED, tags=["videos"])
def add_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.db_add_video(db, video)


@app.get("/test/", tags=["dev"])
def test(db: Session = Depends(get_db)):
    pass
