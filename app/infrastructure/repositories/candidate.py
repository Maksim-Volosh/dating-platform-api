from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.entities import BBoxEntity, UserEntity
from app.domain.interfaces import ICandidateRepository
from app.infrastructure.mappers import UserMapper
from app.infrastructure.models import User


class SQLAlchemyCandidateRepository(ICandidateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_preferences_and_bbox(
        self, user: UserEntity, bbox: BBoxEntity
    ) -> List[UserEntity]:
        prefer_ages = list(range(user.age - 2, user.age + 3))

        if user.prefer_gender != "anyone":
            q = select(User).where(
                User.telegram_id != user.telegram_id,
                User.age.in_(prefer_ages),
                User.gender == user.prefer_gender,
                User.prefer_gender.in_(["anyone", user.gender]),
                User.latitude.between(bbox.min_latitude, bbox.max_latitude),
                User.longitude.between(bbox.min_longitude, bbox.max_longitude),
            )
        else:
            q = select(User).where(
                User.telegram_id != user.telegram_id,
                User.age.in_(prefer_ages),
                User.prefer_gender.in_(["anyone", user.gender]),
                User.latitude.between(bbox.min_latitude, bbox.max_latitude),
                User.longitude.between(bbox.min_longitude, bbox.max_longitude),
            )

        result = await self.session.execute(q)
        user_models = result.scalars().all()
        if not user_models:
            return []

        return [UserMapper.to_entity(user_model) for user_model in user_models]
