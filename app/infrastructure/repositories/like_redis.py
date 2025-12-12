from redis import Redis

from app.domain.interfaces import ILikeCache


class LikeRedisCache(ILikeCache):
    def __init__(self, client: Redis) -> None:
        self.client = client
        
    async def rpush(self, liked_id: int, liker_id: int, timeout=None) -> int:
        key = f"like:{liked_id}"
        set_key = f"set:{liked_id}"
        
        added = await self.client.sadd(set_key, liker_id) # type: ignore
        
        if added == 1:
            await self.client.rpush(key, liker_id) # type: ignore
            if timeout:
                await self.client.expire(key, timeout)
            
        # Get count
        count = await self.client.llen(key) # type: ignore
        if not count:
            return 0

        return count
        
    async def lindex(self, liked_id: int) -> int | None:
        key = f"like:{liked_id}"
        liker_id = await self.client.lindex(key, 0) # type: ignore
        if not liker_id:
            return None
        if type(liker_id) == bytes:
            return int(liker_id)
        else:
            return None
        
    async def lpop(self, liked_id: int) -> int | None:
        key = f"like:{liked_id}"
        set_key = f"set:{liked_id}"
        
        liker_id = await self.client.lpop(key) # type: ignore
        if not liker_id:
            return None
        if type(liker_id) == int:
            await self.client.srem(set_key, liker_id) # type: ignore
            return liker_id
        else:
            return None