from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.keyboards import get_name_keyboard, main_kb


class StartPresenter:

    async def start_registration(self, message: Message, state: FSMContext):
        await message.answer("Привет! Тебя еще нет с нами. Давай зарегистрируемся) ✨")

    async def ask_name(self, message: Message):
        await message.answer(
            "Как тебя зовут?", reply_markup=await get_name_keyboard(message)
        )

    async def send_hello(self, message: Message, user: dict):
        await message.answer(
            f"С возвращением, {html.bold(user['name'])}! 👋", reply_markup=main_kb
        )
