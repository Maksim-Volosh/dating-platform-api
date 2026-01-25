from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)
