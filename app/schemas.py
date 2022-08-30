from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from sqlalchemy import Integer
from typing import Union

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    timestamp: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    timestamp: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Posts: Post
    votes: int

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class VoteDir(int, Enum):
    upvote = 1
    downvote = 0

class Vote(BaseModel):
    post_id: int
    dir: VoteDir