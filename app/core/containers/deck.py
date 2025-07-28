from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases import UserDeckUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import (DeckRedisCache,
                                             SQLAlchemyUserRepository)


async def get_user_deck_use_case(
    db: AsyncSession = Depends(db_helper.session_getter),
    client: Redis = Depends(redis_helper.get_client)
) -> UserDeckUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    cache = DeckRedisCache(client)
    return UserDeckUseCase(
        user_repo=user_repo,
        cache=cache
    )