from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    
class PreferGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    ANYONE = "anyone"


class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]
    city: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender))
    prefer_gender: Mapped[PreferGender] = mapped_column(SQLAlchemyEnum(PreferGender))
    
    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan") # type: ignore


