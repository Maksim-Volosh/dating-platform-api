from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import main_kb, swipe_kb
from app.services import (ack_inbox_item, create_swipe, get_inbox_count,
                          get_next_item, get_user, get_user_photos)
from app.states import LikeSwipeState

router = Router()

@router.message(StateFilter(None), F.text == "🔥")
async def next_like_profile(message: Message, state: FSMContext) -> None:
    if message.from_user:
        if message.text == "🔥":
            await message.answer("✨🔍", reply_markup=swipe_kb)
            
        # --- 1. Get next profile who liked us ---
        inbox_data = await get_next_item(message.from_user.id)
        
        if inbox_data:
            candidate_id = inbox_data.get("candidate_id")
            type_of_inbox = inbox_data.get("type")

            more = await get_inbox_count(message.from_user.id)
            
            # --- 3. Get user data ---
            data = await get_user(candidate_id)
            
            if more and more - 1 > 0:
                msg = f"Кому-то понравилась твоя анкета (И еще {more - 1}):\n\n"
            else:
                msg = "Кому-то понравилась твоя анкета:\n\n"
            
            if data:
                # --- 4. Create caption ---
                caption = (
                    f"{msg}"
                    f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                    f"{html.bold(data['city'])}\n\n"
                    f"{html.italic(data['description'] or 'Без описания')}"
                )
                
                # --- 5. Get user photos ---
                photos = await get_user_photos(data['telegram_id'])
                
                # --- 6. Save current profile id and name ---
                await state.update_data(current_profile_id=candidate_id)
                await state.update_data(current_profile_name=data['name'])
                
                if not photos:
                    await message.answer(caption, reply_markup=swipe_kb)
                    if type_of_inbox == "MATCH":
                        await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={candidate_id}">{data['name']}</a>')
                        await ack_inbox_item(message.from_user.id, candidate_id)
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
                if type_of_inbox == "MATCH":
                    await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={candidate_id}">{data['name']}</a>')
                    await ack_inbox_item(message.from_user.id, candidate_id)
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
    candidate_id = data.get("current_profile_id")
    name = data["current_profile_name"]
    if not name:
        name = "❤️"

    if message.from_user:
        if message.text == "❤️" and candidate_id:
            await state.clear()
            
            # --- Create swipe ---
            await message.answer(f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={candidate_id}">{data["current_profile_name"]}</a>')
            await create_swipe(message.from_user.id, candidate_id, True)
            
            # --- Get count---
            count = await get_inbox_count(candidate_id)
            
            # --- Remove like ---
            await ack_inbox_item(message.from_user.id, candidate_id)
            
            # --- Send message to liked user ---
            if count and count > 1:
                await bot.send_message(candidate_id, f"Эййй, ты понравился {count} людям! Что бы посмотреть их анкеты - выйди в меню ❤️))")
            elif count and count == 1:
                await bot.send_message(candidate_id, f"Эййй, ты понравился {count} человеку! Что бы посмотреть кто это - выйди в меню ❤️))")
            
            # --- Get next like profile ---
            await next_like_profile(message, state)
            
        elif message.text == "👎" and candidate_id:
            await state.clear()
            await create_swipe(message.from_user.id, candidate_id, False)
            await ack_inbox_item(message.from_user.id, candidate_id)
            await next_like_profile(message, state)



def register(dp: Dispatcher) -> None:
    dp.include_router(router)