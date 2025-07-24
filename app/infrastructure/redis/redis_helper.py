from typing import AsyncGenerator
import redis.asyncio as redis
from app.config import settings 

class RedisHelper:
    def __init__(self, url: str) -> None:
        self.client = redis.from_url(url)

    async def dispose(self) -> None:
        await self.client.close()

    async def get_client(self) -> AsyncGenerator[redis.Redis, None]:
        yield self.client


redis_helper = RedisHelper(
    url=str(settings.cache.url)
)
