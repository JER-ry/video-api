import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

import models
import schemas


def db_check_user_existence(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).count() > 0


def db_check_video_existence(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.video_id == video_id).count() > 0


def db_register(db: Session, user: schemas.UserCreate):
    user_id_gen = int(uuid.uuid4()) % 10000000
    while db_check_user_existence(db, user_id_gen):
        user_id_gen = int(uuid.uuid4()) % 10000000
    user_gen = models.User(user_id=user_id_gen)
    db.add(user_gen)
    for item in user.interested_category:
        db.add(models.InterestedCategory(user_id=user_id_gen, interested_category=item))
    db.commit()
    return user_id_gen


def db_check_watched(db: Session, user_id: int, video_id: int):
    return (
        db.query(models.Watch)
        .filter(models.Watch.user_id == user_id, models.Watch.video_id == video_id)
        .count()
        > 0
    )


def db_watch(db: Session, user_id: int, video_id: int):
    if not db_check_watched(db, user_id, video_id):
        db.add(models.Watch(user_id=user_id, video_id=video_id))
        db.commit()


def db_like(db: Session, user_id: int, video_id: int):
    db.query(models.Watch).filter(
        models.Watch.user_id == user_id, models.Watch.video_id == video_id
    ).update({"liked": True})
    db.commit()


def db_unlike(db: Session, user_id: int, video_id: int):
    db.query(models.Watch).filter(
        models.Watch.user_id == user_id, models.Watch.video_id == video_id
    ).update({"liked": False})
    db.commit()


def db_user_watched_any(db: Session, user_id: int):
    return db.query(models.Watch).filter(models.Watch.user_id == user_id).count() > 0


def db_users_interested_category(db: Session, user_id: int):
    return [
        i["interested_category"]
        for i in db.query(models.InterestedCategory.interested_category)
        .filter(models.InterestedCategory.user_id == user_id)
        .all()
    ]


def db_whether_video_watched(db: Session, video_id: int):
    return db.query(models.Watch).filter(models.Watch.video_id == video_id).count() > 0


def db_get_all_watches(db: Session):
    return [(i.user_id, i.video_id, i.liked) for i in db.query(models.Watch).all()]


def db_get_some_new_video_id(
    db: Session, user_id: int, old_video_id: list[int], number_of_videos=30
):
    watched = [
        i["video_id"]
        for i in db.query(models.Watch.video_id)
        .filter(models.Watch.user_id == user_id)
        .all()
    ]
    return [
        i["video_id"]
        for i in db.query(models.Video.video_id)
        .filter(models.Video.video_id.not_in(watched + old_video_id))
        .order_by(random())
        .limit(number_of_videos)
        .all()
    ]


def db_get_video(db: Session, video_id: int, recommended: bool):
    video = (
        db.query(models.Video)
        .filter(models.Video.video_id == video_id)
        .first()
        .to_dict()
    )
    video["recommended"] = recommended
    return video


def db_add_video(db: Session, video: schemas.VideoCreate):
    video_id_gen = int(uuid.uuid4()) % 10000000
    while db_check_video_existence(db, video_id_gen):
        video_id_gen = int(uuid.uuid4()) % 10000000
    video_gen = models.Video(video_id=video_id_gen, **video.dict())
    db.add(video_gen)
    db.commit()
    return video_id_gen
