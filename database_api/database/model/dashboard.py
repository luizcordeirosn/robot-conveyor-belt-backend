from typing import List, Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.model.base import Base

class Dashboard(Base):
    
    __tablename__ = 'dashboards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    image: Mapped[str] = mapped_column(String(255), nullable=False)

    label: Mapped[int] = mapped_column(Integer, nullable=True)

    confidence: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)

    user_id: Mapped[int] = mapped_column('user_id',Integer, ForeignKey('users.id'), nullable=False)

    #relationship
    user: Mapped[List["User"]] = relationship("User", back_populates="dashboards")

    def __repr__(self):
        return f'Dashboard(id = {self.id}, image = {self.image}, label = {self.label}, confidence = {self.confidence}, user_id = {self.user_id})'

from database.model.user import User