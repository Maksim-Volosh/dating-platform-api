from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import UserEntity, UserDistanceEntity


class IDeckCache(ABC):
    @abstractmethod
    async def rpush(self, key: str, users: List[UserDistanceEntity], timeout=None):
        raise NotImplementedError

    @abstractmethod
    async def lpop(self, key: str) -> UserDistanceEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_deck(self, key: str) -> List[UserDistanceEntity] | None:
        raise NotImplementedError
