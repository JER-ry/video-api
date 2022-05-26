from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Watch(Base):
    __tablename__ = "watches"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    video_id = Column(
        Integer, ForeignKey("videos.video_id"), primary_key=True, index=True
    )
    liked = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    videos_watched = relationship("Video", secondary=Watch)
    users_interested_category = relationship("interested_category")


class InterestedCategory(Base):
    __tablename__ = "interested_category"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    interested_category = Column(String, primary_key=True)


class Video(Base):
    __tablename__ = "videos"
    video_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cover = Column(String)
    url = Column(String)
    length_str = Column(String)
    category = Column(String, index=True)
