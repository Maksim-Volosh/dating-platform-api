import random

from app.core.config import settings
from app.domain.entities import UserEntity
from app.domain.interfaces import IDeckCache, ISwipeRepository, IUserRepository


class DeckBuilderService:
    def __init__(self, user_repo: IUserRepository, swipe_repo: ISwipeRepository, cache: IDeckCache) -> None:
        self.user_repo = user_repo
        self.swipe_repo = swipe_repo
        self.cache = cache
        
    async def build(self, user: UserEntity) -> None | bool:
        candidates = await self.user_repo.get_users_by_preferences(user.telegram_id, user.city, user.age, user.gender, user.prefer_gender)
        if candidates is None:
            return None
        
        not_swiped_candidates = [
            candidate for candidate in candidates if await self.swipe_repo.was_swiped(user.telegram_id, candidate.telegram_id) is False
        ]
        if not not_swiped_candidates:
            return None
        random.shuffle(not_swiped_candidates)
        
        key = f"deck:{user.telegram_id}"
        await self.cache.delete(key)
        
        await self.cache.rpush(key, not_swiped_candidates, timeout=settings.deck.timeout)
        return True