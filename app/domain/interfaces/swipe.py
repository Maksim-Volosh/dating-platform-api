from abc import ABC, abstractmethod

from app.domain.entities import NormalizedSwipeEntity
from app.infrastructure.models.swipe import Swipe


class ISwipeRepository(ABC):
    @abstractmethod
    async def create(self, swipe: NormalizedSwipeEntity):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_ids(self, user1_id: int, user2_id: int) -> Swipe | None:
        raise NotImplementedError
    
    async def update(self, swipe: NormalizedSwipeEntity) -> None:
        raise NotImplementedError