import random

from app.core.config import settings
from app.domain.entities import UserEntity
from app.domain.exceptions import NoCandidatesFound, UserNotFoundById
from app.domain.interfaces import IDeckCache, IUserRepository


class DeckBuilderService:
    def __init__(self, user_repo: IUserRepository, cache: IDeckCache) -> None:
        self.user_repo = user_repo
        self.cache = cache
        
    async def build(self, user: UserEntity) -> None:
        candidates = await self.user_repo.get_users_by_preferences(user.telegram_id, user.city, user.age, user.gender, user.prefer_gender)
        if candidates is None:
            raise NoCandidatesFound
        
        random.shuffle(candidates)
        
        key = f"deck:{user.telegram_id}"
        await self.cache.delete(key)
        
        await self.cache.rpush(key, candidates, timeout=settings.deck.timeout)
        return