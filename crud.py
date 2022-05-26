import uuid
from sqlalchemy.orm import Session
import models
import schemas


def db_check_existence(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).count() > 0


def db_register(db: Session, user: schemas.UserCreate):
    user_id_gen = int(uuid.uuid4())
    while db_check_existence(db, user_id_gen):
        user_id_gen = int(uuid.uuid4())
    db_user = models.User(user_id=user_id_gen)
    db.add(db_user)
    for item in user.interested_category:
        db.add(models.InterestedCategory(user_id=user_id_gen, interested_category=item))
    db.commit()
    return db_user


def db_watch(db: Session, user_id: int, video_id: int):
    db.add(models.Watch(user_id=user_id, video_id=video_id))
    db.commit()


def db_like(db: Session, user_id: int, video_id: int):
    db.query(models.Watch).filter(
        models.Watch.user_id == user_id, models.Watch.video_id == video_id
    ).first().liked = True


def db_unlike(db: Session, user_id: int, video_id: int):
    db.query(models.Watch).filter(
        models.Watch.user_id == user_id, models.Watch.video_id == video_id
    ).first().liked = False


def db_user_watched_any(db: Session, user_id: int):
    return (
        len(db.query(models.User).filter(models.User.user_id == user_id).videos_watched)
        > 0
    )


def db_users_interested_category(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(models.User.user_id == user_id)
        .users_interested_category
    )


def db_get_all_watches(db: Session):
    return [(i.user_id, i.video_id, i.liked) for i in db.query(models.Watch).all()]
