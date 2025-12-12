from abc import ABC, abstractmethod


class ILikeCache(ABC):
    @abstractmethod
    async def rpush(self, liked_id: int, liker_id: int, timeout=None) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def lindex(self, liked_id: int) -> int | None:
        raise NotImplementedError
    
    @abstractmethod  
    async def lpop(self, liked_id: int) -> int | None:
        raise NotImplementedError