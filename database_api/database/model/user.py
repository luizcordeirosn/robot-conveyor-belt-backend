from datetime import datetime
from typing import List
from sqlalchemy import Integer, String, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.model.base import Base

class User(Base):
    
    __tablename__ = 'users'

    __table_args__ = (
        CheckConstraint('length(username) <= 255', name='ck_username_length'),
        CheckConstraint('length(password) <= 255', name='ck_password_length'),
    )

    id: Mapped[int] = mapped_column('id', Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column('name', String(255), nullable=False)

    username: Mapped[str] = mapped_column('username', String(255), nullable=False, unique=True)

    password: Mapped[str] = mapped_column('password', String(255))

    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, nullable=False, default=datetime.now())

    #relationship
    logs: Mapped[List["Log"]] = relationship("Log", back_populates='users')
    dashboards: Mapped[List["Dashboard"]] = relationship("Dashboard", back_populates="user")

    def __repr__(self):
        return f'User(id = {self.id}, username = {self.username})'
    
from database.model.log import Log
from database.model.dashboard import Dashboard