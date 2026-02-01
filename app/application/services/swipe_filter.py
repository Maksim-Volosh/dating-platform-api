from app.domain.entities.user import UserEntity
from app.domain.interfaces import ISwipeRepository


class SwipeFilterService:
    def __init__(self, swipe_repo: ISwipeRepository):
        self.swipe_repo = swipe_repo

    async def filter(
        self,
        user_id: int,
        candidates: list[UserEntity],
    ) -> list[UserEntity]:
        swiped_ids = await self.swipe_repo.get_swiped_user_ids(user_id)
        return [c for c in candidates if c.telegram_id not in swiped_ids]
