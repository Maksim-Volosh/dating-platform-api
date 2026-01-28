import random
from typing import List

from app.core.config import settings
from app.domain.entities import UserEntity
from app.domain.interfaces import ICandidateRepository, IDeckCache, ISwipeRepository


class DeckBuilderService:
    def __init__(
        self,
        candidate_repo: ICandidateRepository,
        swipe_repo: ISwipeRepository,
        cache: IDeckCache,
    ) -> None:
        self.candidate_repo = candidate_repo
        self.swipe_repo = swipe_repo
        self.cache = cache

    async def build(self, user: UserEntity) -> None | List[UserEntity]:
        candidates = await self.candidate_repo.get_candidates_by_preferences(
            user.telegram_id, user.age, user.gender, user.prefer_gender
        )
        if candidates is None:
            return None

        not_swiped_candidates = [
            candidate
            for candidate in candidates[: settings.deck.max_size]
            if await self.swipe_repo.was_swiped(user.telegram_id, candidate.telegram_id)
            is False
        ]
        if not not_swiped_candidates:
            return None
        random.shuffle(not_swiped_candidates)

        key = f"deck:{user.telegram_id}"
        await self.cache.delete(key)

        await self.cache.rpush(
            key, not_swiped_candidates, timeout=settings.deck.timeout
        )
        return candidates

    async def _delete_user_from_others_decks(
        self, telegram_id: int, suspicious_users: List[UserEntity]
    ) -> None:
        for user in suspicious_users:
            user_deck = await self.cache.get_deck(f"deck:{user.telegram_id}")
            if user_deck is not None:
                for i, item in enumerate(user_deck):
                    if item.telegram_id == telegram_id:
                        user_deck.pop(i)
                        await self.cache.delete(f"deck:{user.telegram_id}")
                        await self.cache.rpush(
                            f"deck:{user.telegram_id}",
                            user_deck,
                            timeout=settings.deck.timeout,
                        )

    async def build_and_clean_others(self, user: UserEntity) -> None:
        suspicious_users = await self.build(user)

        if suspicious_users is not None:
            await self._delete_user_from_others_decks(
                user.telegram_id, suspicious_users
            )

        return
