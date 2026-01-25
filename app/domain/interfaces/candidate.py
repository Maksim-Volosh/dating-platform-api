from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import UserEntity


class ICandidateRepository(ABC):
    @abstractmethod
    async def get_candidates_by_preferences(
        self, telegram_id: int, city: str, age: int, gender: str, prefer_gender: str
    ) -> List[UserEntity] | None:
        raise NotImplementedError
