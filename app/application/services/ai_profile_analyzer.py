from app.domain.entities import UserEntity
from app.domain.interfaces import IAIClientRepository


class AIProfileAnalyzeService:
    def __init__(
        self,
        ai_repo: IAIClientRepository,
    ):
        self.ai_repo = ai_repo

    def _format_message_by_user(self, user: UserEntity):
        message = f"""
            Ты анализируешь анкету пользователя в дейтинг-приложении.

            Задача:
            Кратко оценить анкету и дать обратную связь.
            
            Оценивай 

            Формат ответа:
            Плюсы:
            1) ...
            2) ...
            3) ...

            Минусы:
            1) ...
            2) ...
            
            Что можно изменить/добавить в описание:
            1) ...
            2) ...

            Ограничения:
            - РОВНО 3 плюса и РОВНО 2 минуса (если плюсов нет, не указывай, не притягивай за уши, плюс ради плюса)
            - ВЕСЬ ответ — не более 2 предложений
            - Общий объём — не более ~600 символов
            - С эмодзи
            - Без морализаторства и советов «как жить»
            - Пиши дружелюбно обращаясь по имены, конструктивно и по делу

            Анкета пользователя:
            Имя: {user.name}
            Описание: {user.description}
        """
        return message

    async def analyze(self, user: UserEntity):

        message = self._format_message_by_user(user)

        return await self.ai_repo.complete(message)
