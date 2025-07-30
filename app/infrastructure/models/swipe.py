from .base import Base
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

class Swipe(Base):
    __tablename__ = "swipe"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user1_id: Mapped[int]
    user1_decision: Mapped[Optional[bool]] = mapped_column(nullable=True)
    user2_id: Mapped[int]
    user2_decision: Mapped[Optional[bool]] = mapped_column(nullable=True)
