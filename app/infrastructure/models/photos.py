from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.telegram_id"))
    user: Mapped["User"] = relationship("User", back_populates="photos")  # type: ignore
