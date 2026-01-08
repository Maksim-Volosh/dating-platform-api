from aiogram import Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.container import container
from app.flows.registartion_flow import RegistrationFlow
from app.states.registration import Registration

router = Router()
flow = RegistrationFlow(container.user_service, container.photo_service)

@router.message(Registration.name)
async def name(message: Message, state: FSMContext):
    await flow.process_name(message, state)

@router.message(Registration.age)
async def age(message: Message, state: FSMContext):
    await flow.process_age(message, state)

@router.message(Registration.city)
async def city(message: Message, state: FSMContext):
    await flow.process_city(message, state)

@router.message(Registration.description)
async def description(message: Message, state: FSMContext):
    await flow.process_description(message, state)

@router.message(Registration.gender)
async def gender(message: Message, state: FSMContext):
    await flow.process_gender(message, state)

@router.message(Registration.prefer_gender)
async def prefer_gender(message: Message, state: FSMContext):
    await flow.process_prefer_gender(message, state)

@router.message(Registration.photos, F.photo)
async def photos(message: Message, state: FSMContext):
    await flow.process_photo(message, state)

@router.message(Registration.photos, F.text.lower() == "завершить")
async def finish(message: Message, state: FSMContext):
    await flow.finish_photos(message, state)
  
    
def register(dp: Dispatcher) -> None:
    dp.include_router(router)