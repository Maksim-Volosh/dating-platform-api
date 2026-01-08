import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.change_profile_presenter import ChangeProfilePresenter
from app.services import update_photos_for_user
from app.services.user.service import UserService
from app.states import Registration, UpdateDescription, UpdatePhotos
from app.validators.registration_validators import validate_description


class ChangeProfileFlow:
    def __init__(self, user_service: UserService):
        self.presenter = ChangeProfilePresenter()
        self.user_service = user_service

    async def restart_registration(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        await self.presenter.restart_registration(message)
        await state.set_state(Registration.name)
        await state.update_data(update=True)
        await self.presenter.ask_name(message)
    
    async def update_photos(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        await self.presenter.ask_photos(message)
        await state.set_state(UpdatePhotos.photos)
    
    async def process_photos(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        photo_ids = data.get("photo_ids", [])

        if len(photo_ids) < 3:
            file_id = message.photo[-1].file_id # type: ignore
            # take the highest quality photo
            photo_ids.append(file_id)

            await state.update_data(photo_ids=photo_ids)
            
            await self.presenter.photo_added(message, len(photo_ids))
            
            if len(photo_ids) == 3:
                await self.finish_photo_upload(message, state)
                
    async def finish_photo_upload(self, message: Message, state: FSMContext):
        data = await state.get_data()
        photo_ids = data.get("photo_ids", [])

        if not photo_ids:
            await self.presenter.no_photos(message)
            return
        
        await asyncio.sleep(0.5)
        await self.presenter.finish_photo_update(message)
        
        if message.from_user is not None:
            await update_photos_for_user(data, message.from_user.id)

        await state.clear()
        
    async def update_profile_description(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        await self.presenter.ask_description(message)
        await state.set_state(UpdateDescription.description)

    async def process_description(self, message: Message, state: FSMContext) -> None:
        if message.text is not None and message.from_user is not None:
            ok, error = validate_description(message.text)
            if not ok and error:
                await self.presenter.send_error(message, error)
                return
            
            await self.user_service.update_description(message.from_user.id, message.text)
            await state.clear()
            await self.presenter.finish_description_update(message)