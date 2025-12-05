import logging

import aiohttp
from aiogram import Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message
from config import API_KEY, API_URL

from app.keyboards.keyboards import get_name_keyboard, main_kb, profile_kb
from app.states.registration import Registration
from app.services import get_user_photos

router = Router()

@router.message(F.text == "Моя анкета")
async def my_profile(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id # type: ignore

    async with aiohttp.ClientSession() as session:
        try:
            # --- 1. Get user data ---
            async with session.get(
                f"{API_URL}/users/{telegram_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 200:
                    await message.answer("Привет! Я тебя не нашёл в базе. Давай зарегистрируемся ✨")
                    await state.set_state(Registration.name)
                    await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))
                    return

                data = await resp.json()
                
            # --- Create caption ---
            caption = (
                f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                f"{html.bold(data['city'])}\n\n"
                f"{html.italic(data['description'] or 'Без описания')}"
            )

            # --- 2. Get user photos ---
            photos = await get_user_photos(telegram_id)

            if not photos:
                await message.answer(caption, reply_markup=main_kb)
                return

            file_ids = [p.get("file_id") for p in photos if p.get("file_id")]

            media_group = [
                InputMediaPhoto(media=fid) for fid in file_ids
            ]

            media_group[0].caption = caption
            media_group[0].parse_mode = "HTML"

            await message.answer_media_group(media_group) # type: ignore
            await message.answer("1. Листать анкеты. \n2. Заполнить анкету заново. \n3. Изменить фотографии. \n4. Изменить описание.", reply_markup=profile_kb)

        except Exception as e:
            logging.error(f"API error: {e}")
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            
@router.message(F.text == "2")
async def restart_registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Ну давай по новой ✨")
    await state.set_state(Registration.name)
    await state.update_data(update=True)
    await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))
      
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)