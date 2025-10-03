from aiogram import Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.keyboards import (get_gender_keyboard,
                                     get_prefer_gender_keyboard, main_kb)
from app.services.create_user import create_user
from app.states.registration import Registration

router = Router()

@router.message(Registration.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Registration.age)
    await message.answer("Сколько тебе лет?", reply_markup=ReplyKeyboardRemove())
    
@router.message(Registration.age)
async def process_age(message: Message, state: FSMContext) -> None:
    try:
        age = int(message.text) # type: ignore
        if not 10 <= age <= 100: 
            await message.answer("⚠️ Укажи возраст числом от 10 до 100.")
            return
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи возраст числом.")
        return

    await state.update_data(age=message.text)
    await state.set_state(Registration.city)
    await message.answer("В каком городе живешь?")
    
@router.message(Registration.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(Registration.description)
    await message.answer("Расскажи немного о себе.")
    
@router.message(Registration.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if len(message.text) > 300: # type: ignore
        await message.answer("⚠️ Описание не должно превышать 300 символов.")
        return
    if len(message.text) < 20: # type: ignore
        await message.answer("⚠️ Описание не должно быть короче 20 символов.")
        return
    await state.update_data(description=message.text)
    await state.set_state(Registration.gender)
    await message.answer("Какой у тебя пол?", reply_markup=await get_gender_keyboard())
    
@router.message(Registration.gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("⚠️ Пожалуйста, выбери валидный пол.")
        return
    await state.update_data(gender=message.text)
    await state.set_state(Registration.prefer_gender)
    await message.answer("Какой у тебя предпочитаемый пол?", reply_markup=await get_prefer_gender_keyboard())
    
@router.message(Registration.prefer_gender)
async def process_prefer_gender(message: Message, state: FSMContext) -> None:
    if message.text not in ["Мужской", "Женский", "Неважно"]:
        await message.answer("⚠️ Пожалуйста, выбери валидный пол.")
        return
    await state.update_data(prefer_gender=message.text)
    data = await state.get_data()
    await message.answer("Отлично! Теперь я знаю о тебе все! 🎉", reply_markup=main_kb)
    await state.clear()
    await create_user(
        data, 
        message.from_user.id # type: ignore
    )
    
def register(dp: Dispatcher) -> None:
    dp.include_router(router)