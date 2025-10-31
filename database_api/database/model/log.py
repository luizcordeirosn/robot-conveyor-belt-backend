from datetime import datetime
from typing import List, Set
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.base import Base


class Log(Base):
    
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    category: Mapped[str] = mapped_column(String(255), nullable=False) # inflamável, não inflamável, reciclável

    color: Mapped[str] = mapped_column(String(255), nullable=False)  # azul, verde, amarelo, branco, preto

    status: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)

    user_id: Mapped[int] = mapped_column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    #relationship
    users: Mapped[List["User"]] = relationship("User", back_populates="logs")

from database.model.user import User