from abc import ABC, abstractmethod

from app.domain.entities import NormalizedSwipeEntity
from app.infrastructure.models.swipe import Swipe


class ISwipeRepository(ABC):
    @abstractmethod
    async def create(self, swipe: NormalizedSwipeEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_ids(self, user1_id: int, user2_id: int) -> Swipe | None:
        raise NotImplementedError
    
    @abstractmethod
    async def was_swiped(self, user_id: int, candidate_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, swipe: NormalizedSwipeEntity) -> None:
        raise NotImplementedError