from cornac.data import Dataset
from cornac.models import BPR
from fastapi import BackgroundTasks, Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bpr = BPR()
dataset = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def train_model(db: Session = Depends(get_db)):
    global dataset  # pylint: disable=global-statement
    dataset = Dataset.build(crud.db_get_all_watches(db))
    try:
        bpr.fit(dataset)
    except:  # pylint: disable=bare-except
        pass


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
def recommend_more(  # pylint: disable=dangerous-default-value
    user_id: int,
    old_video_id: list[int] = [],
    db: Session = Depends(get_db),
):
    final_number_of_videos = 6
    final_video_id = []
    recommended_list = []
    new_video_id = crud.db_get_some_new_video_id(db, user_id, old_video_id)
    if crud.db_user_watched_any(db, user_id):
        try:
            final_video_id += sorted(
                filter(lambda i: crud.db_whether_video_watched(db, i), new_video_id),
                key=lambda i: bpr.score(dataset.uid_map[user_id], dataset.iid_map[i]),
                reverse=True,
            )[:final_number_of_videos]
            recommended_list += [True] * len(final_video_id)
        except:  # pylint: disable=bare-except
            pass
    if len(final_video_id) < final_number_of_videos:
        final_video_id += list(filter(lambda i: i not in final_video_id, new_video_id))[
            : final_number_of_videos - len(final_video_id)
        ]
        recommended_list += [False] * (final_number_of_videos - len(final_video_id))
    return [
        crud.db_get_video(db, i, j) for i, j in zip(final_video_id, recommended_list)
    ]


@app.get("/check_video_existence/{video_id}", tags=["videos"])
def check_video_existence(video_id: int, db: Session = Depends(get_db)):
    return crud.db_check_video_existence(db, video_id)


@app.post("/add_video/", status_code=status.HTTP_201_CREATED, tags=["videos"])
def add_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.db_add_video(db, video)


@app.get("/test/", tags=["dev"], deprecated=True)
def test(db: Session = Depends(get_db)):
    user1 = schemas.UserCreate(interested_categories=["yuri", "new year", "happy"])
    user2 = schemas.UserCreate(interested_categories=["nature", "tv series", "daily"])
    user3 = schemas.UserCreate(interested_categories=["yuri", "tv series", "happy"])
    user_id1 = crud.db_register(db, user1)
    user_id2 = crud.db_register(db, user2)
    user_id3 = crud.db_register(db, user3)
    video1 = schemas.VideoCreate(
        title="yurucamp movie",
        cover="./img/test2.jpg",
        url="https://streamable.com/75b8hw",
        length_str="1:23",
        category="yuri",
    )
    video2 = schemas.VideoCreate(
        title="happy new year",
        cover="./img/test.jpg",
        url="https://streamable.com/idhvqx",
        length_str="122:23",
        category="new year",
    )
    video3 = schemas.VideoCreate(
        title="mountain, lake",
        cover="./img/test7.jpg",
        url="https://streamable.com/81uqs3",
        length_str="0:12",
        category="nature",
    )
    video_id1 = crud.db_add_video(db, video1)
    video_id2 = crud.db_add_video(db, video2)
    video_id3 = crud.db_add_video(db, video3)
    crud.db_watch(db, user_id1, video_id1)
    crud.db_watch(db, user_id1, video_id3)
    crud.db_watch(db, user_id2, video_id2)
    crud.db_watch(db, user_id2, video_id3)
    crud.db_watch(db, user_id3, video_id1)
    crud.db_like(db, user_id1, video_id1)
    crud.db_like(db, user_id3, video_id1)
    crud.db_like(db, user_id2, video_id2)
    crud.db_unlike(db, user_id2, video_id2)
    return {
        "ids": [user_id1, user_id2, user_id3, video_id1, video_id2, video_id3],
        "test1": crud.db_get_some_new_video_id(db, user_id1, []),
        "test2": recommend_more(user_id1, [], db),
    }
