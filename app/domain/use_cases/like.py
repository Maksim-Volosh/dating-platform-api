from app.domain.interfaces import ILikeCache
from app.domain.exceptions import LikeNotFound


class LikeUseCase:
    def __init__(self, cache: ILikeCache) -> None:
        self.cache = cache
        
    async def add_like(self, liked_id: int, liker_id: int) -> int:
        count = await self.cache.rpush(liked_id, liker_id)
        return count
    
    async def get_next_like(self, liked_id: int) -> int:
        liker_id = await self.cache.lindex(liked_id)
        
        if liker_id is None:
            raise LikeNotFound
        
        return liker_id
    
    async def get_count(self, liked_id: int) -> int:
        count = await self.cache.count(liked_id)
        return count
    
    async def remove_like(self, liked_id: int) -> None:
        await self.cache.lpop(liked_id)