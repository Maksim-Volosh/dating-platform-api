from aiogram import Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message
from aiogram import Bot

from app.keyboards.keyboards import main_kb, swipe_kb, like_kb
from app.services import create_swipe, get_next_user, get_user_photos, create_like
from app.states import SwipeState

router = Router()

@router.message(F.text.in_({"1", "Листать анкеты"}))
async def next_profile(message: Message, state: FSMContext) -> None:
    if message.text in ["1", "Листать анкеты"]:
        await message.answer("Окей, поехали! 🚀", reply_markup=swipe_kb)
    
    if message.from_user:
        # --- 1. Get user data ---
        data = await get_next_user(message.from_user.id)
        
        if data:
            # --- Create caption ---
            caption = (
                f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                f"{html.bold(data['city'])}\n\n"
                f"{html.italic(data['description'] or 'Без описания')}"
            )
            
            # --- 2. Get user photos ---
            photos = await get_user_photos(data['telegram_id'])
            await state.update_data(current_profile_id=data['telegram_id'])
            if not photos:
                await message.answer(caption, reply_markup=swipe_kb)
                await state.set_state(SwipeState.swipe)
                return

            file_ids = [p.get("file_id") for p in photos if p.get("file_id")]

            media_group = [
                InputMediaPhoto(media=fid) for fid in file_ids
            ]

            media_group[0].caption = caption
            media_group[0].parse_mode = "HTML"

            await message.answer_media_group(media_group) # type: ignore
            await state.set_state(SwipeState.swipe)
        else:
            await message.answer("Извини но сейчас нету подходящих анкет по твоим параметрам. Попробуй позже.", reply_markup=main_kb)


@router.message(SwipeState.swipe)
async def swipe(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    liked_id = data.get("current_profile_id")

    if message.from_user:
        if message.text == "❤️" and liked_id:
            await state.clear()
            
            # --- Create swipe ---
            await message.answer("Отлично, лайк отправлен ✨ Ждем взаимного лайка")
            await create_swipe(message.from_user.id, liked_id, True)
            
            # --- Create like and get count---
            count = await create_like(message.from_user.id, liked_id)
            
            # --- Send message to liked user ---
            if count and count > 1:
                await bot.send_message(liked_id, f"Еййй, ты понравился {count} девушкам! ❤️))", reply_markup=like_kb)
            elif count and count == 1:
                await bot.send_message(liked_id, f"Еййй, ты понравился {count} девушке! ❤️))", reply_markup=like_kb)
            
            # --- Get next profile ---
            await next_profile(message, state)
            
        elif message.text == "👎" and liked_id:
            await state.clear()
            await create_swipe(message.from_user.id, liked_id, False)
            await next_profile(message, state)



def register(dp: Dispatcher) -> None:
    dp.include_router(router)