from app.application.services import (DeckBuilderService,
                                      GeoCandidateFilterService,
                                      SwipeFilterService)
from app.core.config import settings
from app.domain.entities import UserDistanceEntity, UserEntity
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)
from app.domain.interfaces import (ICandidateRepository, IDeckCache,
                                   IUserRepository)
from app.domain.services.bounding_box import bounding_box
from app.domain.services.haversine import haversine


class UserUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def get_by_id(self, telegram_id: int) -> UserEntity:
        user: UserEntity | None = await self.repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById()
        return user

    async def get_all(self) -> list[UserEntity]:
        users = await self.repo.get_all()
        if users is None:
            raise UsersNotFound()
        return users


class CreateUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        deck_builder: DeckBuilderService,
        candidate_repo: ICandidateRepository,
        geo_filter: GeoCandidateFilterService,
        swipe_filter: SwipeFilterService
    ) -> None:
        self.user_repo = user_repo
        self.deck_builder = deck_builder
        self.candidate_repo = candidate_repo
        self.geo_filter = geo_filter
        self.swipe_filter = swipe_filter

    async def execute(self, user: UserEntity) -> UserEntity:
        created_user = await self.user_repo.create(user)
        if created_user is None:
            raise UserAlreadyExists()

        if created_user:
            bbx = bounding_box(
                created_user.latitude, created_user.longitude, settings.deck.radius_steps_km[-1]
            )
            candidates = await self.candidate_repo.find_by_preferences_and_bbox(
                created_user, bbx
            )
            swipe_filtered_candidates = await self.swipe_filter.filter(
                created_user.telegram_id, candidates
            )
            geo_filtered_candidates = await self.geo_filter.filter(
                created_user, swipe_filtered_candidates
            )
            if geo_filtered_candidates:
                await self.deck_builder.build(created_user, geo_filtered_candidates)

        return created_user


class UpdateUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        deck_builder: DeckBuilderService,
        cache: IDeckCache,
        candidate_repo: ICandidateRepository,
        geo_filter: GeoCandidateFilterService,
        swipe_filter: SwipeFilterService
        
    ) -> None:
        self.user_repo = user_repo
        self.deck_builder = deck_builder
        self.cache = cache
        self.candidate_repo = candidate_repo
        self.geo_filter = geo_filter
        self.swipe_filter = swipe_filter

    async def execute(self, telegram_id: int, update: UserEntity) -> UserEntity:
        updated_user = await self.user_repo.update(telegram_id, update)
        if updated_user is None:
            raise UserNotFoundById()

        if updated_user:
            bbx = bounding_box(
                updated_user.latitude, updated_user.longitude, settings.deck.radius_steps_km[-1]
            )
            candidates = await self.candidate_repo.find_by_preferences_and_bbox(
                updated_user, bbx
            )
            swipe_filtered_candidates = await self.swipe_filter.filter(
                updated_user.telegram_id, candidates
            )
            geo_filtered_candidates = await self.geo_filter.filter(
                updated_user, swipe_filtered_candidates
            )
            if geo_filtered_candidates:
                await self.deck_builder.build(updated_user, geo_filtered_candidates)
                await self.deck_builder.clean_others(updated_user, candidates)

        return updated_user


class UpdateUserDescriptionUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, telegram_id: int, description: str) -> UserEntity:
        updated_user = await self.user_repo.update_description(telegram_id, description)
        if updated_user is None:
            raise UserNotFoundById()

        return updated_user


class GetUserProfileViewUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, viewer_id: int, candidate_id: int):
        viewer = await self.user_repo.get_by_id(viewer_id)
        candidate = await self.user_repo.get_by_id(candidate_id)

        if viewer is None or candidate is None:
            raise UserNotFoundById()
        
        distance = haversine(
            viewer.latitude,
            viewer.longitude,
            candidate.latitude,
            candidate.longitude,
        )

        return UserDistanceEntity(
            telegram_id=candidate.telegram_id,
            name=candidate.name,
            age=candidate.age,
            distance=distance,
            gender=candidate.gender,
            prefer_gender=candidate.prefer_gender,
            description=candidate.description,
        )