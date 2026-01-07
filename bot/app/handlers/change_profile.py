import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.keyboards import get_name_keyboard, main_kb, photo_kb
from app.services import update_description, update_photos_for_user
from app.states import Registration, UpdateDescription, UpdatePhotos

from app.flows.change_profile import ChangeProfileFlow

router = Router()
flow = ChangeProfileFlow()
            
@router.message(StateFilter(None), F.text == "2")
async def restart_registration(message: Message, state: FSMContext) -> None:
    await flow.restart_registration(message, state)
    
@router.message(StateFilter(None), F.text == "3")
async def update_photos(message: Message, state: FSMContext) -> None:
    await flow.update_photos(message, state)

@router.message(UpdatePhotos.photos, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    await flow.process_photos(message, state)
      
@router.message(UpdatePhotos.photos, F.text.lower() == "завершить")
async def finish_photo_upload(message: Message, state: FSMContext):
    await flow.finish_photo_upload(message, state)
    
@router.message(StateFilter(None), F.text == "4")
async def update_profile_description(message: Message, state: FSMContext) -> None:
    await flow.update_profile_description(message, state)
            
@router.message(UpdateDescription.description)
async def process_description(message: Message, state: FSMContext) -> None:
    await flow.process_description(message, state)
    
def register(dp: Dispatcher) -> None:
    dp.include_router(router)