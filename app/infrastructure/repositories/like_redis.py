from redis import Redis

from app.domain.interfaces import ILikeCache


class LikeRedisCache(ILikeCache):
    def __init__(self, client: Redis) -> None:
        self.client = client
        
    async def rpush(self, key: str, liker_id: int, timeout=None) -> int:
        await self.client.rpush(key, liker_id) # type: ignore
        if timeout:
            await self.client.expire(key, timeout)
            
        # Get count
        count = await self.client.llen(key) # type: ignore
        if not count:
            return 0

        return count
        
    async def lindex(self, key: str) -> int | None:
        liker_id = await self.client.lindex(key, 0) # type: ignore
        if not liker_id:
            return None
        if type(liker_id) == bytes:
            return int(liker_id)
        else:
            return None
        
    async def lpop(self, key: str) -> int | None:
        liker_id = await self.client.lpop(key) # type: ignore
        if not liker_id:
            return None
        if type(liker_id) == int:
            return liker_id
        else:
            return None