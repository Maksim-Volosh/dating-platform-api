from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases import SwipeUserUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.repositories import (SQLAlchemySwipeRepository,
                                             SQLAlchemyUserRepository)


async def get_swipe_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> SwipeUserUseCase:
    swipe_repo = SQLAlchemySwipeRepository(db)
    return SwipeUserUseCase(
        swipe_repo=swipe_repo
    )