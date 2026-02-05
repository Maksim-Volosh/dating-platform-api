from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.interfaces import IAIClientRepository, IUserRepository


class AIMatchOpenerService:
    def __init__(
        self,
        ai_repo: IAIClientRepository,
        user_repo: IUserRepository
    ):
        self.ai_repo = ai_repo
        self.user_repo = user_repo
        
    def _format_message_by_users(self, liker_user: UserEntity, candidate_user: UserEntity) -> str:
        message = f"""
            Ты помогаешь написать первое сообщение в дейтинг-приложении после взаимного лайка.

            Контекст:
            - Это первое сообщение, оно должно быть живым и естественным
            - Без пошлости, без клише, без банальных фраз
            - Сообщение должно выглядеть так, как будто его написал реальный человек

            Данные:
            Моя анкета:
            Имя: {liker_user.name}
            Описание: {liker_user.description}
            Возраст: {liker_user.age}
            Гендер: {liker_user.gender}
            
            Анкета собеседника:
            Имя: {candidate_user.name}
            Описание: {candidate_user.description}
            Возраст: {candidate_user.age}
            Гендер: {candidate_user.gender}
            
            Возраст и гендер даны только как контекст, не делай сообщения, основанные ТОЛЬКО на них.

            Если у собеседника нет описания или оно пустое:
            - придумай лёгкое, дружелюбное и человеческое сообщение
            - допускается лёгкий юмор или нейтральное любопытство

            Формат ответа (строго соблюдай):
            Вариант 1: ...
            Вариант 2: ...
            Вариант 3: ...

            Ограничения:
            - РОВНО 3 варианта
            - Каждое сообщение — 1 предложение
            - Без эмодзи
            - Без вопросов про «чем занимаешься»
            - Без советов и метакомментариев
            - Общий объём ответа — до ~600 символов
            - Пиши на том же языке, что и анкеты

        """
        return message
    
    async def generate(self, liker_id: int, candidate_id: int):
        liker_user = await self.user_repo.get_by_id(liker_id)
        candidate_user = await self.user_repo.get_by_id(candidate_id)
        
        if liker_user is None or candidate_user is None:
            raise UserNotFoundById()
        
        message = self._format_message_by_users(liker_user, candidate_user)
        
        return await self.ai_repo.complete(message)