from fastapi import Depends
from redis import Redis

from app.domain.use_cases import InboxUseCase
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import InboxRedisCache


async def get_inbox_use_case(
    client: Redis = Depends(redis_helper.get_client)
) -> InboxUseCase:
    cache = InboxRedisCache(client)
    return InboxUseCase(
        cache=cache
    )


