import random
from typing import List

from app.core.config import settings
from app.domain.entities import UserDistanceEntity, UserEntity
from app.domain.interfaces import (ICandidateRepository, IDeckCache,
                                   ISwipeRepository)


class DeckBuilderService:
    def __init__(
        self,
        cache: IDeckCache,
    ) -> None:
        self.cache = cache

    async def build(self, user: UserEntity, candidates: List[UserDistanceEntity]) -> List[UserDistanceEntity]:
        random.shuffle(candidates[: settings.deck.max_size])

        key = f"deck:{user.telegram_id}"
        await self.cache.delete(key)

        await self.cache.rpush(
            key, candidates, timeout=settings.deck.timeout
        )
        return candidates

    async def clean_others(
        self, user: UserEntity, suspicious_users: List[UserEntity]
    ) -> None:
        for susp_user in suspicious_users:
            user_deck = await self.cache.get_deck(f"deck:{susp_user.telegram_id}")
            if user_deck is not None:
                for i, item in enumerate(user_deck):
                    if item.telegram_id == user.telegram_id:
                        user_deck.pop(i)
                        await self.cache.delete(f"deck:{susp_user.telegram_id}")
                        await self.cache.rpush(
                            f"deck:{susp_user.telegram_id}",
                            user_deck,
                            timeout=settings.deck.timeout,
                        )
