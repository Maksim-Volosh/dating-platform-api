import logging

import aiohttp
from aiogram import Dispatcher, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import API_KEY, API_URL

from app.keyboards.keyboards import get_name_keyboard, main_kb
from app.states.registration import Registration

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id # type: ignore
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/users/{telegram_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.answer(f"С возвращением, {html.bold(data['name'])}! 👋", reply_markup=main_kb)
                else:
                    await message.answer("Привет! Я тебя не нашёл в базе. Давай зарегистрируемся ✨")
                    await state.set_state(Registration.name)
                    await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))

        except Exception as e:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            logging.error(f"API error: {e}")
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)