import logging
import os
import tempfile

import aiohttp
from aiogram import Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, Message
from config import API_KEY, API_URL

from app.keyboards.keyboards import get_name_keyboard, main_kb
from app.states.registration import Registration

router = Router()

@router.message(F.text == "Моя анкета")
async def my_profile(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id # type: ignore

    async with aiohttp.ClientSession() as session:
        try:
            # --- 1. Получаем данные пользователя ---
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
                caption = (
                    f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                    f"{html.bold(data['city'])}\n\n{html.bold(data['description'] or 'Без описания')}"
                )

            # --- 2. Получаем фото пользователя ---
            async with session.get(
                f"{API_URL}/users/{telegram_id}/photos",
                headers={"x-api-key": API_KEY}
            ) as photo_resp:
                if photo_resp.status == 200:
                    photos_data = await photo_resp.json()
                    photos = photos_data.get("photos", [])

                    if photos:
                        media = []
                        tmp_files = []  # сохраняем, чтобы потом удалить

                        for i, p in enumerate(photos):
                            async with session.get("http://localhost:8000" + p["url"]) as resp:
                                if resp.status == 200:
                                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                                    tmp_file.write(await resp.read())
                                    tmp_file.close()

                                    # caption добавляем только к первому фото
                                    if i == 0:
                                        media.append(InputMediaPhoto(
                                            media=FSInputFile(tmp_file.name),
                                            caption=caption,
                                            parse_mode="HTML"
                                        ))
                                    else:
                                        media.append(InputMediaPhoto(media=FSInputFile(tmp_file.name)))

                                    tmp_files.append(tmp_file.name)

                        if media:
                            await message.answer_media_group(media)
                            await message.answer("⬆️ Вот твоя анкета", reply_markup=main_kb)

                        # удаляем файлы после отправки
                        for f in tmp_files:
                            os.remove(f)

                    else:
                        await message.answer(caption, reply_markup=main_kb)
                else:
                    await message.answer(caption, reply_markup=main_kb)

        except Exception as e:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            logging.error(f"API error: {e}")
            
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)