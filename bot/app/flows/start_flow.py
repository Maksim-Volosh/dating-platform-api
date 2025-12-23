from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.presenters.start_presenter import StartPresenter
from app.services import get_user

class StartFlow:
    def __init__(self):
        self.presenter = StartPresenter()

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        telegram_id = message.from_user.id # type: ignore
        
        user = await get_user(telegram_id)
        
        if user is None:
            await self.presenter.start_registration(message, state)
            return

        if user is False:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            return

        await self.presenter.send_hello(
            message=message,
            user=user
        )
        
        