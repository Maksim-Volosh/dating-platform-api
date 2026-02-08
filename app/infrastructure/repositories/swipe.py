from sqlalchemy import select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import FullSwipeEntity, NormalizedSwipeEntity
from app.domain.interfaces import ISwipeRepository
from app.infrastructure.models import Swipe


class SQLAlchemySwipeRepository(ISwipeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, swipe: NormalizedSwipeEntity) -> FullSwipeEntity:
        swipe_model = Swipe(
            user1_id=swipe.user1_id,
            user2_id=swipe.user2_id,
            user1_decision=swipe.decision if swipe.liker_is_user1 else None,
            user2_decision=swipe.decision if not swipe.liker_is_user1 else None,
        )
        self.session.add(swipe_model)
        await self.session.commit()
        return FullSwipeEntity(
            user1_id=swipe.user1_id,
            user1_decision=swipe.decision if swipe.liker_is_user1 else None,
            user2_id=swipe.user2_id,
            user2_decision=swipe.decision if not swipe.liker_is_user1 else None,
        )

    async def get_by_ids(self, user1_id: int, user2_id: int) -> Swipe | None:
        q = select(Swipe).where(Swipe.user1_id == user1_id, Swipe.user2_id == user2_id)
        result = await self.session.execute(q)
        swipe_model = result.scalars().one_or_none()
        if swipe_model is None:
            return None
        return swipe_model

    async def update(
        self, exist_swipe: Swipe, swipe: NormalizedSwipeEntity
    ) -> FullSwipeEntity:
        if swipe.liker_is_user1:
            exist_swipe.user1_decision = swipe.decision
        if not swipe.liker_is_user1:
            exist_swipe.user2_decision = swipe.decision
        await self.session.commit()
        return FullSwipeEntity(
            user1_id=exist_swipe.user1_id,
            user1_decision=exist_swipe.user1_decision,
            user2_id=exist_swipe.user2_id,
            user2_decision=exist_swipe.user2_decision,
        )

    async def get_swiped_user_ids(self, user_id: int) -> set[int]:
        q1 = select(Swipe.user2_id).where(
            Swipe.user1_id == user_id,
            Swipe.user1_decision.isnot(None),
        )

        q2 = select(Swipe.user1_id).where(
            Swipe.user2_id == user_id,
            Swipe.user2_decision.isnot(None),
        )

        q = union_all(q1, q2)
        result = await self.session.execute(q)
        return set(result.scalars().all())
