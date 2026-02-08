from openai import AsyncOpenAI
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import (AIMatchOpenerService,
                                      AIProfileAnalyzeService,
                                      DeckBuilderService,
                                      GeoCandidateFilterService,
                                      InboxOnSwipeService, SwipeFilterService)
from app.application.use_cases import (AIMatchOpenerUseCase,
                                       AIProfileAnalizeUseCase,
                                       CreateUserUseCase,
                                       DeleteUserPhotosUseCase,
                                       GetUserProfileViewUseCase, InboxUseCase,
                                       RetrieveUserPhotosUseCase,
                                       SwipeUserUseCase,
                                       UpdateUserDescriptionUseCase,
                                       UpdateUserPhotosUseCase,
                                       UpdateUserUseCase,
                                       UploadUserPhotosUseCase,
                                       UserDeckUseCase, UserUseCase)
from app.core.config import settings
from app.infrastructure.rate_limit import RateLimiter
from app.infrastructure.repositories import (DeckRedisCache, InboxRedisCache,
                                             OpenRouterClient,
                                             SQLAlchemyCandidateRepository,
                                             SQLAlchemyPhotoRepository,
                                             SQLAlchemySwipeRepository,
                                             SQLAlchemyUserRepository)


class Container:
    def __init__(self, session: AsyncSession, redis: Redis, ai_client: AsyncOpenAI):
        self.session = session
        self.redis = redis
        self.ai_client = ai_client

    # ---------- repositories ----------

    def user_repo(self):
        return SQLAlchemyUserRepository(self.session)

    def swipe_repo(self):
        return SQLAlchemySwipeRepository(self.session)

    def candidate_repo(self):
        return SQLAlchemyCandidateRepository(self.session)

    def photo_repo(self):
        return SQLAlchemyPhotoRepository(self.session)
    
    def openrouter_client(self):
        return OpenRouterClient(self.ai_client, settings.ai.timeout)

    # ---------- caches ----------

    def deck_cache(self):
        return DeckRedisCache(self.redis)

    def inbox_cache(self):
        return InboxRedisCache(self.redis)

    # ---------- rate limit ----------
    
    def rate_limiter(self):
        return RateLimiter(self.redis)
    
    # ---------- services ----------

    def deck_builder(self):
        return DeckBuilderService(
            cache=self.deck_cache()
        )
    def geo_filter(self):
        return GeoCandidateFilterService()
    
    def swipe_filter(self):
        return SwipeFilterService(
            swipe_repo=self.swipe_repo()
        )
    
    def inbox_on_swipe_service(self):
        return InboxOnSwipeService(inbox_cache=self.inbox_cache())
    
    def ai_profile_analize_service(self):
        return AIProfileAnalyzeService(
            ai_repo=self.openrouter_client()
        )

    def ai_match_opener_service(self):
        return AIMatchOpenerService(
            ai_repo=self.openrouter_client()
        )
    
    # ---------- use cases ----------

    def user_use_case(self):
        return UserUseCase(repo=self.user_repo())
    
    def get_user_profile_view_use_case(self):
        return GetUserProfileViewUseCase(user_repo=self.user_repo())

    def create_user_use_case(self):
        return CreateUserUseCase(
            user_repo=self.user_repo(),
            deck_builder=self.deck_builder(),
            candidate_repo=self.candidate_repo(),
            geo_filter=self.geo_filter(),
            swipe_filter=self.swipe_filter(),
        )

    def update_user_use_case(self):
        return UpdateUserUseCase(
            user_repo=self.user_repo(),
            deck_builder=self.deck_builder(),
            cache=self.deck_cache(),
            candidate_repo=self.candidate_repo(),
            geo_filter=self.geo_filter(),
            swipe_filter=self.swipe_filter(),
        )

    def update_user_description_use_case(self):
        return UpdateUserDescriptionUseCase(user_repo=self.user_repo())

    def user_deck_use_case(self):
        return UserDeckUseCase(
            cache=self.deck_cache(),
            deck_builder=self.deck_builder(),
            candidate_repo=self.candidate_repo(),
            geo_filter=self.geo_filter(),
            swipe_filter=self.swipe_filter(),
        )

    def swipe_user_use_case(self):
        return SwipeUserUseCase(
            swipe_repo=self.swipe_repo(),
            inbox_service=self.inbox_on_swipe_service()
        )

    def inbox_use_case(self):
        return InboxUseCase(cache=self.inbox_cache())

    def delete_user_photos_use_case(self):
        return DeleteUserPhotosUseCase(photo_repo=self.photo_repo())

    def retrieve_user_photos_use_case(self):
        return RetrieveUserPhotosUseCase(photo_repo=self.photo_repo())

    def update_user_photos_use_case(self):
        return UpdateUserPhotosUseCase(photo_repo=self.photo_repo())

    def upload_user_photos_use_case(self):
        return UploadUserPhotosUseCase(photo_repo=self.photo_repo())
    
    def ai_profile_analize_use_case(self):
        return AIProfileAnalizeUseCase(
            ai_analize_service=self.ai_profile_analize_service(),
            user_repo=self.user_repo()
        )
        
    def ai_match_opener_use_case(self):
        return AIMatchOpenerUseCase(
            ai_opener_service=self.ai_match_opener_service(),
            user_repo=self.user_repo()
        )
