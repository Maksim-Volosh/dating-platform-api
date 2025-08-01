import random

from app.core.config import settings
from app.domain.entities import UserEntity
from app.domain.exceptions import NoCandidatesFound, UserNotFoundById
from app.domain.interfaces import IDeckCache, IUserRepository


class DeckBuilderService:
    def __init__(self, user_repo: IUserRepository, cache: IDeckCache) -> None:
        self.user_repo = user_repo
        self.cache = cache
        
    async def build(self, telegram_id: int) -> None:
        user: UserEntity | None = await self.user_repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        
        candidates = await self.user_repo.get_users_by_preferences(telegram_id, user.city, user.age, user.gender, user.prefer_gender)
        if candidates is None:
            raise NoCandidatesFound
        
        random.shuffle(candidates)
        
        key = f"deck:{telegram_id}"
        
        await self.cache.rpush(key, candidates, timeout=settings.deck.timeout)
        return