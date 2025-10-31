from pydantic import BaseModel
from datetime import datetime


class Dashboard(BaseModel):
    id: int
    image: str
    label: int
    confidence: float
    user_id: int
    created_at: datetime

class DashCreate(Dashboard):
    pass

class DashResponse(Dashboard):
    id: int
    image: str
    label: int
    confidence: float
    created_at: datetime