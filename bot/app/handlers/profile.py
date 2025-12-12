from aiogram import Dispatcher, F, Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import get_name_keyboard, main_kb, profile_kb
from app.services import get_user, get_user_photos
from app.states.registration import Registration

router = Router()

@router.message(StateFilter(None), F.text == "Моя анкета")
async def my_profile(message: Message, state: FSMContext) -> None:
    # --- 1. Get user ---
    telegram_id = message.from_user.id # type: ignore
    data = await get_user(telegram_id)

    if data: 
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
        
    elif data is None:
        await message.answer("Привет! Тебя еще нет с нами. Давай зарегистрируемся) ✨")
        await state.set_state(Registration.name)
        await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message)) 
        
    elif data == False:
        await message.answer("⚠️ Ошибка при соединении с сервером.")
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)