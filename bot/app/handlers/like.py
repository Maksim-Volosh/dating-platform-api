from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import main_kb, swipe_kb
from app.services import (create_like, create_swipe, get_next_like, get_user,
                          get_user_photos, is_match, remove_like)
from app.states import LikeSwipeState

router = Router()

@router.message(StateFilter(None), F.text == "🔥")
async def next_like_profile(message: Message, state: FSMContext) -> None:
    if message.from_user:
        if message.text == "🔥":
            await message.answer("✨🔍", reply_markup=swipe_kb)
            
        # --- 1. Get next profile who liked us ---
        liker_id = await get_next_like(message.from_user.id)
        
        if liker_id:
            # --- 2. Check is match with him ---
            is_match_result = await is_match(message.from_user.id, liker_id)
            
            # --- 3. Get user data ---
            data = await get_user(liker_id)
            
            if data:
                # --- 4. Create caption ---
                caption = (
                    f"Кому-то понравилась твоя анкета:\n\n"
                    f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                    f"{html.bold(data['city'])}\n\n"
                    f"{html.italic(data['description'] or 'Без описания')}"
                )
                
                # --- 5. Get user photos ---
                photos = await get_user_photos(data['telegram_id'])
                
                # --- 6. Save current profile id and name ---
                await state.update_data(current_profile_id=liker_id)
                await state.update_data(current_profile_name=data['name'])
                
                if not photos:
                    await message.answer(caption, reply_markup=swipe_kb)
                    if is_match_result:
                        await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={liker_id}">{data['name']}</a>')
                        await remove_like(message.from_user.id)
                        await state.update_data(not_first_like=True)
                        await next_like_profile(message, state)
                        return
                    else:
                        await state.set_state(LikeSwipeState.swipe)
                    return

                file_ids = [p.get("file_id") for p in photos if p.get("file_id")]

                media_group = [
                    InputMediaPhoto(media=fid) for fid in file_ids
                ]

                media_group[0].caption = caption
                media_group[0].parse_mode = "HTML"

                await message.answer_media_group(media_group) # type: ignore
                if is_match_result:
                    await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={liker_id}">{data['name']}</a>')
                    await remove_like(message.from_user.id)
                    await state.update_data(not_first_like=True)
                    await next_like_profile(message, state)
                    return
                await state.set_state(LikeSwipeState.swipe)
            else:
                await message.answer("Извини но что то пошло не так. Попробуй позже.", reply_markup=main_kb)
        else:
            if message.text == "🔥" and not (await state.get_data()).get("not_first_like", False):
                await message.answer("Уже не актуально", reply_markup=main_kb)
            else:
                await message.answer("На сегодня это все 🙃 Идем дальше?", reply_markup=main_kb)


@router.message(LikeSwipeState.swipe)
async def swipe(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    liked_id = data.get("current_profile_id")
    name = data["current_profile_name"]
    if not name:
        name = "❤️"

    if message.from_user:
        if message.text == "❤️" and liked_id:
            await state.clear()
            
            # --- Create swipe ---
            await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={liked_id}">{data["current_profile_name"]}</a>')
            await create_swipe(message.from_user.id, liked_id, True)
            
            # --- Create like and get count---
            count = await create_like(message.from_user.id, liked_id)
            
            # --- Remove like ---
            await remove_like(message.from_user.id)
            
            # --- Send message to liked user ---
            if count and count > 1:
                await bot.send_message(liked_id, f"Эййй, ты понравился {count} людям! Что бы посмотреть их анкеты - выйди в меню ❤️))")
            elif count and count == 1:
                await bot.send_message(liked_id, f"Эййй, ты понравился {count} человеку! Что бы посмотреть кто это - выйди в меню ❤️))")
            
            # --- Get next like profile ---
            await next_like_profile(message, state)
            
        elif message.text == "👎" and liked_id:
            await state.clear()
            await create_swipe(message.from_user.id, liked_id, False)
            await remove_like(message.from_user.id)
            await next_like_profile(message, state)



def register(dp: Dispatcher) -> None:
    dp.include_router(router)