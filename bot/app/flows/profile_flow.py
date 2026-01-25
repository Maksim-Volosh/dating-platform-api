from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.profile_presenter import ProfilePresenter
from app.services import PhotoService, UserService, InboxService
from app.states.registration import Registration


class ProfileFlow:
    def __init__(
        self,
        user_service: UserService,
        photo_service: PhotoService,
        inbox_service: InboxService,
    ):
        self.presenter = ProfilePresenter()
        self.user_service = user_service
        self.photo_service = photo_service
        self.inbox_service = inbox_service

    async def show_my_profile(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        telegram_id = message.from_user.id  # type: ignore
        data = await self.user_service.get_user(telegram_id)

        if data is None:
            await self.presenter.start_registration(message, state)
            await state.set_state(Registration.name)
            await self.presenter.ask_name(message)
            return

        if data is False:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            return

        photos = await self.photo_service.get_user_photos(telegram_id)
        inbox_count = await self.inbox_service.get_inbox_count(telegram_id)

        await self.presenter.show_profile(
            message=message, user=data, photos=photos, inbox_count=inbox_count
        )
