from enum import Enum
from typing import List, Optional

from sqlalchemy import UUID
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String
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

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]
    city: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender))
    prefer_gender: Mapped[PreferGender] = mapped_column(SQLAlchemyEnum(PreferGender))
    
    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="photos")