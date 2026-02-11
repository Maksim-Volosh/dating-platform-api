from aiogram import Bot
from aiogram.types import Message

from app.keyboards.keyboards import main_kb


class AIPresenter:
    async def send_wait(self, message: Message) -> None:
        await message.answer(
            "Подожди немного пока генерирую... Это может занять некоторое время",
            reply_markup=None,
        )

    async def send_call_wait(self, bot: Bot, chat_id: int) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text="Подожди немного пока генерирую... Это может занять некоторое время",
        )

    async def send_error(self, message: Message) -> None:
        await message.answer(
            "Извини но что то пошло не так. Попробуй позже.", reply_markup=main_kb
        )

    async def send_call_error(self, bot: Bot, chat_id: int) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text="Извини но что то пошло не так. Попробуй позже.",
        )

    async def send_limit(self, message: Message) -> None:
        await message.answer(
            "За сегодня слишком много запросов. Попробуй позже :)",
            reply_markup=main_kb,
        )

    async def send_call_limit(self, bot: Bot, chat_id: int) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text="За сегодня слишком много запросов. Попробуй позже :)",
        )

    async def send_result(self, message: Message, result) -> None:
        await message.answer(
            f"Отлично! Готово! \n\n{result["response"]}", reply_markup=main_kb
        )

    async def send_call_result(self, bot: Bot, chat_id: int, result) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text=f"Отлично! Готово! \n\n{result["response"]}",
        )
