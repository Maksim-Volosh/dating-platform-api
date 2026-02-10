import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.registration_presenter import RegistrationPresenter
from app.services import PhotoService, UserService
from app.states.registration import Registration
from app.validators.registration_validators import (
    validate_age,
    validate_description,
    validate_gender,
    validate_prefer_gender,
)


class RegistrationFlow:
    def __init__(self, user_service: UserService, photo_service: PhotoService):
        self.user_service = user_service
        self.photo_service = photo_service
        self.presenter = RegistrationPresenter()

    async def process_name(self, message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Registration.age)
        await self.presenter.ask_age(message)

    async def process_age(self, message: Message, state: FSMContext):
        ok, error = validate_age(message.text)
        if not ok and error:
            await message.answer(error)
            return

        await state.update_data(age=message.text)
        await state.set_state(Registration.location)
        await self.presenter.ask_location(message)

    async def process_location(self, message: Message, state: FSMContext):
        if message.location:
            await state.update_data(
                latitude=message.location.latitude, longitude=message.location.longitude
            )
            await state.set_state(Registration.description)
            await self.presenter.ask_description(message)
        else:
            await message.answer("Пожалуйста, отправь свое местоположение")

    async def process_description(self, message: Message, state: FSMContext):
        ok, error = validate_description(message.text)
        if not ok and error:
            await message.answer(error)
            return

        await state.update_data(description=message.text)
        await state.set_state(Registration.gender)
        await self.presenter.ask_gender(message)

    async def process_gender(self, message: Message, state: FSMContext):
        ok, error = validate_gender(message.text)
        if not ok and error:
            await message.answer(error)
            return

        await state.update_data(gender=message.text)
        await state.set_state(Registration.prefer_gender)
        await self.presenter.ask_prefer_gender(message)

    async def process_prefer_gender(self, message: Message, state: FSMContext):
        ok, error = validate_prefer_gender(message.text)
        if not ok and error:
            await message.answer(error)
            return

        await state.update_data(prefer_gender=message.text)
        await state.set_state(Registration.photos)
        await self.presenter.ask_photos(message)

    async def process_photo(self, message: Message, state: FSMContext):
        data = await state.get_data()
        photo_ids = data.get("photo_ids", [])

        if len(photo_ids) >= 3:
            return

        # take the highest quality photo
        photo_ids.append(message.photo[-1].file_id)  # type: ignore
        await state.update_data(photo_ids=photo_ids)

        await self.presenter.photo_added(message, len(photo_ids))

        if len(photo_ids) == 3:
            await self.finish_photos(message, state)

    async def finish_photos(self, message: Message, state: FSMContext):
        data = await state.get_data()
        photo_ids = data.get("photo_ids", [])

        if not photo_ids:
            await message.answer("Ты не отправил ни одной фотографии 🙃")
            return

        await asyncio.sleep(0.5)
        await self.presenter.finish_registration(message)

        if message.from_user:
            if data.get("update"):
                await self.user_service.update_user_profile(data, message.from_user.id)
                await self.photo_service.update_photos_for_user(
                    data, message.from_user.id
                )
            else:
                await self.user_service.create_user_profile(data, message.from_user.id)
                await self.photo_service.create_photos_for_user(
                    data, message.from_user.id
                )

        await state.clear()
