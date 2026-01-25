from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import (
    get_name_keyboard,
    main_kb,
    profile_kb,
    profile_with_likes_kb,
)


class ProfilePresenter:

    async def start_registration(self, message: Message, state: FSMContext):
        await message.answer("Привет! Тебя еще нет с нами. Давай зарегистрируемся) ✨")

    async def ask_name(self, message: Message):
        await message.answer(
            "Как тебя зовут?", reply_markup=await get_name_keyboard(message)
        )

    async def show_profile(
        self, message: Message, user: dict, photos, inbox_count: int | None
    ):
        caption = (
            f"{html.bold(user['name'])}, {html.bold(str(user['age']))}, "
            f"{html.bold(user['city'])}\n\n"
            f"{html.italic(user['description'] or 'Без описания')}"
        )

        if photos:
            file_ids = [p["file_id"] for p in photos if p.get("file_id")]
            media = [InputMediaPhoto(media=fid) for fid in file_ids]

            media[0].caption = caption
            media[0].parse_mode = "HTML"

            await message.answer_media_group(media)  # type: ignore
        else:
            await message.answer(caption, reply_markup=main_kb)

        await self._send_menu(message, inbox_count)

    async def _send_menu(self, message: Message, count: int | None):
        if count and count > 1:
            text = f"🔥. Посмотреть {count} лайков.\n2. Заполнить анкету заново.\n3. Изменить фотографии.\n4. Изменить описание.\n***\n💤. Обновить меню"
            kb = profile_with_likes_kb
        elif count == 1:
            text = f"🔥. Посмотреть {count} лайк.\n2. Заполнить анкету заново.\n3. Изменить фотографии.\n4. Изменить описание.\n***\n💤. Обновить меню"
            kb = profile_with_likes_kb
        else:
            text = "1. Листать анкеты.\n2. Заполнить анкету заново.\n3. Изменить фотографии.\n4. Изменить описание.\n***\n💤. Обновить меню"
            kb = profile_kb

        await message.answer(text, reply_markup=kb)
