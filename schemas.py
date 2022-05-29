from pydantic import BaseModel


class UserCreate(BaseModel):
    interested_category: list[str]


class VideoCreate(BaseModel):
    title: str
    cover: str
    url: str
    length_str: str
    category: str
