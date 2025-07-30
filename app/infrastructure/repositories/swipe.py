from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import NormalizedSwipeEntity
from app.domain.interfaces import ISwipeRepository
from app.infrastructure.models import Swipe


class SQLAlchemySwipeRepository(ISwipeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, swipe: NormalizedSwipeEntity):
        swipe_model = Swipe(
            user1_id=swipe.user1_id,
            user2_id=swipe.user2_id,
            user1_decision=swipe.decision if swipe.liker_is_user1 else None,
            user2_decision=swipe.decision if not swipe.liker_is_user1 else None 
        )
        self.session.add(swipe_model)
        await self.session.commit()
        
    async def get_by_ids(self, user1_id: int, user2_id: int) -> Swipe | None:
        q = select(Swipe).where(Swipe.user1_id == user1_id, Swipe.user2_id == user2_id)
        result = await self.session.execute(q)
        swipe_model = result.scalars().one_or_none()
        if swipe_model is None:
            return None
        return swipe_model
    
    async def update(self, swipe: NormalizedSwipeEntity):
        swipe_model = await self.get_by_ids(swipe.user1_id, swipe.user2_id)
        if swipe_model is None:
            return None
        if swipe.liker_is_user1:
            swipe_model.user1_decision = swipe.decision 
        if not swipe.liker_is_user1:
            swipe_model.user2_decision = swipe.decision
        await self.session.commit()