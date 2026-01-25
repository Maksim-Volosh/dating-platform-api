from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities import FullSwipeEntity, NormalizedSwipeEntity


class ISwipeRepository(ABC):
    @abstractmethod
    async def create(self, swipe: NormalizedSwipeEntity) -> FullSwipeEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, user1_id: int, user2_id: int) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def was_swiped(self, user_id: int, candidate_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, exist_swipe, swipe: NormalizedSwipeEntity
    ) -> FullSwipeEntity:
        raise NotImplementedError
