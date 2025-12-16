from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import InboxOnSwipeService
from app.application.use_cases import SwipeUserUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import (InboxRedisCache,
                                             SQLAlchemySwipeRepository)


async def get_swipe_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter),
    client: Redis = Depends(redis_helper.get_client)
) -> SwipeUserUseCase:
    swipe_repo = SQLAlchemySwipeRepository(db)
    inbox_cache = InboxRedisCache(client)
    inbox_service = InboxOnSwipeService(inbox_cache=inbox_cache)
    return SwipeUserUseCase(
        swipe_repo=swipe_repo,
        inbox_service=inbox_service
    )