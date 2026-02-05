from app.application.services import AIProfileAnalizeService, AIMatchOpenerService
from app.domain.exceptions import AIUnavailableError


class AIProfileAnalizeUseCase:
    def __init__(self, ai_analize_service: AIProfileAnalizeService) -> None:
        self.ai_analize_service = ai_analize_service
        
    async def execute(self, telegram_id: int):
        result = await self.ai_analize_service.analize(telegram_id)
        
        if result is None:
            raise AIUnavailableError()
        
        return result
    
class AIMatchOpenerUseCase:
    def __init__(self, ai_opener_service: AIMatchOpenerService) -> None:
        self.ai_opener_service = ai_opener_service
        
    async def execute(self, liker_id: int, candidate_id: int):
        result = await self.ai_opener_service.generate(liker_id, candidate_id)
        
        if result is None:
            raise AIUnavailableError()
        
        return result