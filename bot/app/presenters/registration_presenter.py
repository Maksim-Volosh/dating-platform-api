from aiogram.types import Message, ReplyKeyboardRemove
from app.keyboards.keyboards import (
    get_gender_keyboard,
    get_prefer_gender_keyboard,
    main_kb,
    photo_kb,
)

class RegistrationPresenter:

    async def ask_age(self, message: Message):
        await message.answer("Сколько тебе лет?", reply_markup=ReplyKeyboardRemove())

    async def ask_city(self, message: Message):
        await message.answer("В каком городе живешь?")

    async def ask_description(self, message: Message):
        await message.answer("Расскажи немного о себе.")

    async def ask_gender(self, message: Message):
        await message.answer("Какой у тебя пол?", reply_markup=await get_gender_keyboard())

    async def ask_prefer_gender(self, message: Message):
        await message.answer(
            "Какой у тебя предпочитаемый пол?",
            reply_markup=await get_prefer_gender_keyboard()
        )

    async def ask_photos(self, message: Message):
        await message.answer(
            "Отлично, теперь пришли мне свои фотографии (до 3х)",
            reply_markup=photo_kb
        )

    async def photo_added(self, message: Message, count: int):
        await message.answer(f"Фото добавлено ({count}/3).", reply_markup=photo_kb)

    async def finish_registration(self, message: Message):
        await message.answer(
            "Отлично! Теперь я знаю о тебе всё! 🎉",
            reply_markup=main_kb
        )
