from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
