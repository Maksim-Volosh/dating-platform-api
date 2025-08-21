from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services import DeckBuilderService
from app.domain.use_cases import UserDeckUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import (DeckRedisCache,
                                             SQLAlchemySwipeRepository,
                                             SQLAlchemyUserRepository)


async def get_user_deck_use_case(
    db: AsyncSession = Depends(db_helper.session_getter),
    client: Redis = Depends(redis_helper.get_client)
) -> UserDeckUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    swipe_repo = SQLAlchemySwipeRepository(db)
    cache = DeckRedisCache(client)
    deck_builder = DeckBuilderService(user_repo, swipe_repo, cache)
    return UserDeckUseCase(
        user_repo=user_repo,
        cache=cache,
        deck_builder=deck_builder
    )