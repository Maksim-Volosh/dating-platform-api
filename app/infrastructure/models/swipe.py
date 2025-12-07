from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Swipe(Base):
    __tablename__ = "swipe"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user1_id: Mapped[int] = mapped_column(BigInteger)
    user1_decision: Mapped[Optional[bool]] = mapped_column(nullable=True)
    user2_id: Mapped[int] = mapped_column(BigInteger)
    user2_decision: Mapped[Optional[bool]] = mapped_column(nullable=True)
