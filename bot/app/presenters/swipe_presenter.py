from aiogram import Bot, html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import main_kb, swipe_kb


class SwipePresenter:
    async def start_swiping(self, message: Message) -> None:
        await message.answer("✨🔍", reply_markup=swipe_kb)
       
    async def _create_profile_caption(self, user: dict) -> str:
        caption = (
            f"{html.bold(user['name'])}, {html.bold(str(user['age']))}, "
            f"{html.bold(user['city'])}\n\n"
            f"{html.italic(user['description'] or 'Без описания')}"
        )
        
        return caption
        
    async def send_profile_without_photos(self, message: Message, user: dict) -> None:
        caption = await self._create_profile_caption(user)
        await message.answer(caption, reply_markup=swipe_kb)
    
    async def send_profile(self, message: Message, user: dict, photos) -> None:
        caption = await self._create_profile_caption(user)
        
        file_ids = [p.get("file_id") for p in photos if p.get("file_id")]

        media_group = [
            InputMediaPhoto(media=fid) for fid in file_ids
        ]

        media_group[0].caption = caption
        media_group[0].parse_mode = "HTML"

        await message.answer_media_group(media_group) # type: ignore

    async def send_no_more_profiles(self, message: Message) -> None:
        await message.answer("Извини но сейчас нету подходящих анкет по твоим параметрам. Попробуй позже.", reply_markup=main_kb)
    
    async def send_successful_swipe(self, message: Message) -> None:
        await message.answer("Отлично, лайк отправлен ✨ Ждем взаимного лайка")
    
    async def send_notification(self, count: int | None, liked_id: int, bot: Bot) -> None:
        try:
            if count and count > 1:
                await bot.send_message(liked_id, f"Эййй, ты понравился {count} людям! Что бы посмотреть их анкеты - выйди в меню ❤️))")
            elif count and count == 1:
                await bot.send_message(liked_id, f"Эййй, ты понравился {count} человеку! Что бы посмотреть кто это - выйди в меню ❤️))")
        except TelegramBadRequest:
            pass