
from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.interfaces import IDeckCache, IUserRepository
from app.domain.services import DeckBuilderService


class UserDeckUseCase:
    def __init__(self, user_repo: IUserRepository, cache: IDeckCache, deck_builder: DeckBuilderService) -> None:
        self.user_repo = user_repo
        self.cache = cache
        self.deck_builder = deck_builder
        
    async def next(self, telegram_id: int) -> UserEntity:
        key = f"deck:{telegram_id}"
        user = await self.cache.lpop(key)
        if user is None:
            await self.deck_builder.build(telegram_id)
            user = await self.cache.lpop(key)
            if user is None:
                raise UserNotFoundById
        return user