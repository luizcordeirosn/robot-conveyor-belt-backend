from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime


class UserCreate(UserBase):
    username: str
    password: str
    created_at: datetime

class UserResponse(UserBase):
    id: int
    username: str
    password: str
    created_at: datetime