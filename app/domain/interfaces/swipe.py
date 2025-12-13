from abc import ABC, abstractmethod

from app.domain.entities import (FullSwipeEntity, NormalizedMatchEntity,
                                 NormalizedSwipeEntity)
from app.infrastructure.models.swipe import Swipe


class ISwipeRepository(ABC):
    @abstractmethod
    async def create(self, swipe: NormalizedSwipeEntity) -> FullSwipeEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_ids(self, user1_id: int, user2_id: int) -> Swipe | None:
        raise NotImplementedError
    
    @abstractmethod
    async def was_swiped(self, user_id: int, candidate_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, exist_swipe: Swipe, swipe: NormalizedSwipeEntity) -> FullSwipeEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def is_match(self, swipe: NormalizedMatchEntity) -> bool:
        raise NotImplementedError