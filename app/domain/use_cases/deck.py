from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions import NoCandidatesFound
from app.domain.interfaces import IUserRepository, IDeckCache


class UserDeckUseCase:
    def __init__(self, user_repo: IUserRepository, cache: IDeckCache) -> None:
        self.user_repo = user_repo
        self.cache = cache
        
    async def build(self, telegram_id: int) -> None:
        user: UserEntity | None = await self.user_repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        
        candidates = await self.user_repo.get_users_by_preferences(user.city, user.age, user.gender, user.prefer_gender)
        if candidates is None:
            raise NoCandidatesFound
        
        key = f"deck:{telegram_id}"
        
        await self.cache.rpush(key, candidates, timeout=60 * 60 * 6)
        return
    
    async def next(self, telegram_id: int) -> UserEntity:
        key = f"deck:{telegram_id}"
        user = await self.cache.lpop(key)
        if user is None:
            await self.build(telegram_id)
            user = await self.cache.lpop(key)
            if user is None:
                raise UserNotFoundById
        return user