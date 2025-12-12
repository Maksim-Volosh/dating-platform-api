from abc import ABC, abstractmethod


class ILikeCache(ABC):
    @abstractmethod
    async def rpush(self, key: str, liker_id: int, timeout=None) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def lindex(self, key: str) -> int | None:
        raise NotImplementedError
    
    @abstractmethod  
    async def lpop(self, key: str) -> int | None:
        raise NotImplementedError