from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.start_presenter import StartPresenter
from app.services.user.service import UserService
from app.states.registration import Registration


class StartFlow:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.presenter = StartPresenter()

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        telegram_id = message.from_user.id  # type: ignore

        user = await self.user_service.get_user(telegram_id)

        if user is None:
            await self.presenter.start_registration(message, state)
            await state.set_state(Registration.name)
            await self.presenter.ask_name(message)
            return

        if user is False:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            return

        await self.presenter.send_hello(message=message, user=user)
