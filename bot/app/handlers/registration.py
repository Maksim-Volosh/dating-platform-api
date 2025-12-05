import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.keyboards import (get_gender_keyboard,
                                     get_prefer_gender_keyboard, main_kb,
                                     photo_kb)
from app.services import (create_photos_for_user, create_user_profile,
                          update_photos_for_user, update_user_profile)
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
    await state.set_state(Registration.photos)
    await message.answer("Отлично, теперь пришли мне свои фотографии где можно увидеть твою красоту!) Фотографий не должно быть больше 3х")
    

@router.message(Registration.photos, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])


    if len(photo_ids) < 3:
        file_id = message.photo[-1].file_id # type: ignore
        # take the highest quality photo
        photo_ids.append(file_id)

        await state.update_data(photo_ids=photo_ids)
        if len(photo_ids) == 3:
            await message.answer(
                f"Фото добавлено ({len(photo_ids)}/3)."
            )
            await finish_photo_upload(message, state)
        elif len(photo_ids) < 3:
            await message.answer(
                f"Фото добавлено ({len(photo_ids)}/3). Отправь ещё или нажми «Завершить», когда закончишь.", reply_markup=photo_kb
            )
    
@router.message(Registration.photos, F.text.lower() == "завершить")
async def finish_photo_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])

    if not photo_ids:
        await message.answer("Ты не отправил ни одной фотографии 🙃")
        return
    
    await asyncio.sleep(0.5)
    await message.answer("Отлично! Теперь я знаю о тебе всё! 🎉", reply_markup=main_kb)
    
    if message.from_user is not None:
        if data.get("update"):
            await update_user_profile(data, message.from_user.id)
            await update_photos_for_user(data, message.from_user.id)
        else:
            await create_user_profile(data, message.from_user.id)
            await create_photos_for_user(data, message.from_user.id)

    await state.clear()
    
def register(dp: Dispatcher) -> None:
    dp.include_router(router)
    
    