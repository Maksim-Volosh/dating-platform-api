
from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.deck import NoCandidatesFound
from app.domain.interfaces import IDeckCache
from app.application.services import DeckBuilderService


class UserDeckUseCase:
    def __init__(self, cache: IDeckCache, deck_builder: DeckBuilderService) -> None:
        self.cache = cache
        self.deck_builder = deck_builder
        
    async def next(self, user: UserEntity) -> UserEntity:
        key = f"deck:{user.telegram_id}"
        user_entity = await self.cache.lpop(key)
        if user_entity is None:
            res = await self.deck_builder.build(user)
            if res is None:
                raise NoCandidatesFound()
            user_entity = await self.cache.lpop(key)
            if user_entity is None:
                raise UserNotFoundById()
        return user_entity