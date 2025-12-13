from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases import SwipeMatchUserCase, SwipeUserUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.repositories import SQLAlchemySwipeRepository


async def get_swipe_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> SwipeUserUseCase:
    swipe_repo = SQLAlchemySwipeRepository(db)
    return SwipeUserUseCase(
        swipe_repo=swipe_repo
    )
    
async def get_swipe_match_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> SwipeMatchUserCase:
    swipe_repo = SQLAlchemySwipeRepository(db)
    return SwipeMatchUserCase(
        swipe_repo=swipe_repo
    )