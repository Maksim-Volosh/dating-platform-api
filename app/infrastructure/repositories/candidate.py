from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.entities import UserEntity
from app.domain.interfaces import ICandidateRepository
from app.infrastructure.mappers import UserMapper
from app.infrastructure.models import User


class SQLAlchemyCandidateRepository(ICandidateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def get_candidates_by_preferences(self, telegram_id: int, city: str, age: int, gender: str, prefer_gender: str) -> List[UserEntity] | None:
        prefer_ages = list(range(age - 2, age + 3))
        
        if prefer_gender != 'anyone':
            q = select(User).where(
                User.telegram_id != telegram_id,
                User.city == city,
                User.age.in_(prefer_ages),
                User.gender == prefer_gender,
                User.prefer_gender.in_(['anyone', gender])
            )
        else:
            q = select(User).where(
                User.telegram_id != telegram_id,
                User.city == city,
                User.age.in_(prefer_ages),
                User.prefer_gender.in_(['anyone', gender])
            )
            
        result = await self.session.execute(q)
        user_models = result.scalars().all()
        if not user_models:
            return None
        
        return [UserMapper.to_entity(user_model) for user_model in user_models]