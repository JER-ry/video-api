from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    interested_category: list[str]


class User(UserBase):
    user_id: int
    users_interested_category: list[str]

    class Config:
        orm_mode = True


class VideoBase(BaseModel):
    title: str
    cover: str
    url: str
    length_str: str
    category: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    video_id: int

    class Config:
        orm_mode = True
