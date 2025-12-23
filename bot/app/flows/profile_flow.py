from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.presenters.profile_presenter import ProfilePresenter
from app.services import get_inbox_count, get_user, get_user_photos

class ProfileFlow:
    def __init__(self):
        self.presenter = ProfilePresenter()

    async def show_my_profile(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        telegram_id = message.from_user.id  # type: ignore
        data = await get_user(telegram_id)

        if data is None:
            await self.presenter.start_registration(message, state)
            return

        if data is False:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            return

        photos = await get_user_photos(telegram_id)
        inbox_count = await get_inbox_count(telegram_id)

        await self.presenter.show_profile(
            message=message,
            user=data,
            photos=photos,
            inbox_count=inbox_count
        )
