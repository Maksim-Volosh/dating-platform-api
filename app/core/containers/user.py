from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import DeckBuilderService
from app.application.use_cases import (CreateUserUseCase,
                                       UpdateUserDescriptionUseCase,
                                       UpdateUserUseCase, UserUseCase)
from app.infrastructure.db import db_helper
from app.infrastructure.redis import redis_helper
from app.infrastructure.repositories import (DeckRedisCache,
                                             SQLAlchemyCandidateRepository,
                                             SQLAlchemySwipeRepository,
                                             SQLAlchemyUserRepository)


async def get_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UserUseCase:
    repo = SQLAlchemyUserRepository(db)
    return UserUseCase(repo=repo)

async def get_create_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter),
    client: Redis = Depends(redis_helper.get_client)
) -> CreateUserUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    swipe_repo = SQLAlchemySwipeRepository(db)
    cache = DeckRedisCache(client)
    candidate_repo = SQLAlchemyCandidateRepository(db)
    deck_builder = DeckBuilderService(candidate_repo, swipe_repo, cache)
    return CreateUserUseCase(user_repo=user_repo, deck_builder=deck_builder)

async def get_update_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter),
    client: Redis = Depends(redis_helper.get_client)
) -> UpdateUserUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    swipe_repo = SQLAlchemySwipeRepository(db)
    cache = DeckRedisCache(client)
    candidate_repo = SQLAlchemyCandidateRepository(db)
    deck_builder = DeckBuilderService(candidate_repo, swipe_repo, cache)
    return UpdateUserUseCase(user_repo=user_repo, deck_builder=deck_builder, cache=cache)

async def get_update_user_description_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UpdateUserDescriptionUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    return UpdateUserDescriptionUseCase(user_repo=user_repo)