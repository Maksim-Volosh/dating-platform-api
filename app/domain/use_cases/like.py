from app.domain.interfaces import ILikeCache
from app.domain.exceptions import LikeNotFound


class LikeUseCase:
    def __init__(self, cache: ILikeCache) -> None:
        self.cache = cache
        
    async def add_like(self, liked_id: int, liker_id: int) -> int:
        key = f"like:{liked_id}"
        count = await self.cache.rpush(key, liker_id)
        
        return count
    
    async def get_next_like(self, liked_id: int) -> int:
        key = f"like:{liked_id}"
        liker_id = await self.cache.lindex(key)
        
        if liker_id is None:
            raise LikeNotFound
        
        return liker_id
    
    async def remove_like(self, liked_id: int) -> None:
        key = f"like:{liked_id}"
        await self.cache.lpop(key)