from app.application.services import AIMatchOpenerService, AIProfileAnalyzeService
from app.domain.exceptions import AIUnavailableError, UserNotFoundById
from app.domain.interfaces import IUserRepository


class AIProfileAnalizeUseCase:
    def __init__(
        self, ai_analize_service: AIProfileAnalyzeService, user_repo: IUserRepository
    ) -> None:
        self.ai_analize_service = ai_analize_service
        self.user_repo = user_repo

    async def execute(self, telegram_id: int):
        user = await self.user_repo.get_by_id(telegram_id)

        if user is None:
            raise UserNotFoundById()

        result = await self.ai_analize_service.analyze(user)

        if result is None:
            raise AIUnavailableError()

        return result


class AIMatchOpenerUseCase:
    def __init__(
        self, ai_opener_service: AIMatchOpenerService, user_repo: IUserRepository
    ) -> None:
        self.ai_opener_service = ai_opener_service
        self.user_repo = user_repo

    async def execute(self, liker_id: int, candidate_id: int):
        liker_user = await self.user_repo.get_by_id(liker_id)
        candidate_user = await self.user_repo.get_by_id(candidate_id)

        if liker_user is None or candidate_user is None:
            raise UserNotFoundById()

        result = await self.ai_opener_service.generate(liker_user, candidate_user)

        if result is None:
            raise AIUnavailableError()

        return result
