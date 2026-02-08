from redis import Redis

from app.domain.exceptions.rate_limit import RateLimitTooManyRequests


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def hit(self, key: str, limit: int, window_sec: int) -> None:
        """
        Raises RateLimitTooManyRequests if limit exceeded
        """
        current = await self._redis.incr(key)

        if current == 1:
            await self._redis.expire(key, window_sec)

        if current > limit:
            ttl = await self._redis.ttl(key)
            raise RateLimitTooManyRequests()
