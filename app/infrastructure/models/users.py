from typing import List, Optional

from sqlalchemy import BigInteger
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities import Gender, PreferGender

from .base import Base


class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]
    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)
    description: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender))
    prefer_gender: Mapped[PreferGender] = mapped_column(SQLAlchemyEnum(PreferGender))

    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan")  # type: ignore
