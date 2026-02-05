from app.application.services import AIProfileAnalizeService
from app.domain.exceptions import AIUnavailableError


class AIProfileAnalizeUseCase:
    def __init__(self, ai_analize_service: AIProfileAnalizeService) -> None:
        self.ai_analize_service = ai_analize_service
        
    async def execute(self, telegram_id: int):
        result = await self.ai_analize_service.analize(telegram_id)
        
        if result is None:
            raise AIUnavailableError()
        
        return result