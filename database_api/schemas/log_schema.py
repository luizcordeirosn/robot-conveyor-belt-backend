from pydantic import BaseModel
from datetime import datetime


class Log(BaseModel):
    id: int
    category: str
    color: str
    status: str
    user_id: int
    created_at: datetime

class LogCreate(Log):
    pass

class LogResponse(Log):
    id: int
    created_at: datetime