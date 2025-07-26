from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.use_cases import UserUseCase
from app.infrastructure.db import db_helper
from app.infrastructure.repositories import SQLAlchemyUserRepository

async def get_user_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UserUseCase:
    repo = SQLAlchemyUserRepository(db)
    return UserUseCase(repo=repo)