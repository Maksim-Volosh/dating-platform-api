from app.application.services import (DeckBuilderService,
                                      GeoCandidateFilterService,
                                      SwipeFilterService)
from app.core.config import settings
from app.domain.entities import UserDistanceEntity, UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.deck import NoCandidatesFound
from app.domain.interfaces import ICandidateRepository, IDeckCache
from app.domain.interfaces.candidate import ICandidateRepository
from app.domain.services.boundaring_box import bounding_box


class UserDeckUseCase:
    def __init__(
        self,
        cache: IDeckCache,
        deck_builder: DeckBuilderService,
        candidate_repo: ICandidateRepository,
        geo_filter: GeoCandidateFilterService,
        swipe_filter: SwipeFilterService
    ) -> None:
        self.cache = cache
        self.deck_builder = deck_builder
        self.candidate_repo = candidate_repo
        self.geo_filter = geo_filter
        self.swipe_filter = swipe_filter

    async def next(self, user: UserEntity) -> UserDistanceEntity:
        key = f"deck:{user.telegram_id}"
        user_entity = await self.cache.lpop(key)
        if user_entity is None:            
            bbx = bounding_box(
                user.latitude, user.longitude, settings.deck.radius_steps_km[-1]
            )
            candidates = await self.candidate_repo.find_by_preferences_and_bbox(
                user, bbx
            )
            swipe_filtered_candidates = await self.swipe_filter.filter(
                user.telegram_id, candidates
            )
            geo_filtered_candidates = await self.geo_filter.filter(
                user, swipe_filtered_candidates
            )
            if not geo_filtered_candidates:
                raise NoCandidatesFound()
            
            await self.deck_builder.build(user, geo_filtered_candidates)
            
            user_entity = await self.cache.lpop(key)
            if user_entity is None:
                raise UserNotFoundById()
            
        return user_entity
