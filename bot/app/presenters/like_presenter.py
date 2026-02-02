from aiogram import Bot, html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, Message

from app.keyboards.keyboards import main_kb, swipe_kb


class LikePresenter:
    async def start_swiping(self, message: Message) -> None:
        await message.answer("✨🔍", reply_markup=swipe_kb)

    async def _create_profile_caption(self, user: dict, more: int | None) -> str:
        if more and more - 1 > 0:
            msg = f"Кому-то понравилась твоя анкета (И еще {more - 1}):\n\n"
        else:
            msg = "Кому-то понравилась твоя анкета:\n\n"

        caption = (
            f"{msg}"
            f"{html.bold(user['name'])}, {html.bold(str(user['age']))}, "
            f"📍 {html.bold(user['distance'])} {html.bold("км")}\n\n"
            f"{html.italic(user['description'] or 'Без описания')}"
        )

        return caption

    async def send_profile_without_photos(
        self, message: Message, user: dict, more: int | None
    ) -> None:
        caption = await self._create_profile_caption(user, more)
        await message.answer(caption, reply_markup=swipe_kb)

    async def send_profile(
        self, message: Message, user: dict, photos, more: int | None
    ) -> None:
        caption = await self._create_profile_caption(user, more)

        file_ids = [p.get("file_id") for p in photos if p.get("file_id")]

        media_group = [InputMediaPhoto(media=fid) for fid in file_ids]

        media_group[0].caption = caption
        media_group[0].parse_mode = "HTML"

        await message.answer_media_group(media_group)  # type: ignore

    async def send_match(self, message: Message, candidate_id: int, name: str) -> None:
        await message.answer(
            f'Отлично, надеюсь вы хорошо проведете время! \n\nНачинайте общаться -> <a href="tg://user?id={candidate_id}">{name}</a>'
        )

    async def send_error_getting_profile(self, message: Message) -> None:
        await message.answer(
            "Извини но что то пошло не так. Попробуй позже.", reply_markup=main_kb
        )

    async def send_not_actual_data(self, message: Message) -> None:
        await message.answer("Уже не актуально", reply_markup=main_kb)

    async def send_no_more_profiles_today(self, message: Message) -> None:
        await message.answer("На сегодня это все 🙃 Идем дальше?", reply_markup=main_kb)

    async def send_notification(
        self, count: int | None, liked_id: int, bot: Bot
    ) -> None:
        try:
            if count and count > 1:
                await bot.send_message(
                    liked_id,
                    f"Эййй, ты понравился {count} людям! Что бы посмотреть их анкеты - выйди в меню ❤️))",
                )
            elif count and count == 1:
                await bot.send_message(
                    liked_id,
                    f"Эййй, ты понравился {count} человеку! Что бы посмотреть кто это - выйди в меню ❤️))",
                )
        except TelegramBadRequest:
            pass
