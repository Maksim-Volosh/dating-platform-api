from fastapi import Depends
from redis import Redis

from app.domain.use_cases import LikeUseCase
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import LikeRedisCache


async def get_like_use_case(
    client: Redis = Depends(redis_helper.get_client)
) -> LikeUseCase:
    cache = LikeRedisCache(client)
    return LikeUseCase(
        cache=cache
    )