import asyncio
import logging
import os
import sys
import tempfile
from os import getenv

import aiohttp
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (FSInputFile, InputMediaPhoto, KeyboardButton,
                           Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN", "key")
API_URL = getenv("API_URL", "http://localhost:8000/api/v1")
API_KEY = getenv("API_KEY", "k")


dp = Dispatcher()

class Registration(StatesGroup):
    name = State()
    age = State()
    city = State()
    description = State()
    gender = State()
    prefer_gender = State()
    
async def get_name_keyboard(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"{message.from_user.first_name}")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def get_gender_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мужской")
    kb.button(text="Женский")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def get_prefer_gender_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мужской")
    kb.button(text="Женский")
    kb.button(text="Неважно")
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Моя анкета"), KeyboardButton(text="Листать анкеты")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
}
PREFER_GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
    "Неважно": "anyone",
}

async def create_user(data: dict, telegram_id: int) -> bool:
    payload = {
        "telegram_id": telegram_id,
        "name": data["name"],
        "age": int(data["age"]),
        "city": data["city"],
        "description": data["description"],
        "gender": GENDER_MAP[data["gender"]],
        "prefer_gender": PREFER_GENDER_MAP[data["prefer_gender"]],
    }
    print(payload)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/users/",
                headers={"x-api-key": API_KEY},
                json=payload,
            ) as resp:
                if resp.status == 201:
                    return True
                else:
                    logging.error(f"API error: {await resp.text()}")
                    return False


        except Exception as e:
            logging.error(f"API error: {e}")
    return False



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    
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
                    await message.answer("Как тебя зовут?", reply_markup= await get_name_keyboard(message))

        except Exception as e:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            logging.error(f"API error: {e}")
            
@dp.message(Registration.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Registration.age)
    await message.answer("Сколько тебе лет?", reply_markup=ReplyKeyboardRemove())
    
@dp.message(Registration.age)
async def process_age(message: Message, state: FSMContext) -> None:
    try:
        age = int(message.text)
        if not 10 <= age <= 100: 
            await message.answer("⚠️ Укажи возраст числом от 10 до 100.")
            return
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи возраст числом.")
        return

    await state.update_data(age=message.text)
    await state.set_state(Registration.city)
    await message.answer("В каком городе живешь?")
    
@dp.message(Registration.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(Registration.description)
    await message.answer("Расскажи немного о себе.")
    
@dp.message(Registration.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if len(message.text) > 300:
        await message.answer("⚠️ Описание не должно превышать 300 символов.")
        return
    if len(message.text) < 20:
        await message.answer("⚠️ Описание не должно быть короче 20 символов.")
        return
    await state.update_data(description=message.text)
    await state.set_state(Registration.gender)
    await message.answer("Какой у тебя пол?", reply_markup=await get_gender_keyboard())
    
@dp.message(Registration.gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("⚠️ Пожалуйста, выбери валидный пол.")
        return
    await state.update_data(gender=message.text)
    await state.set_state(Registration.prefer_gender)
    await message.answer("Какой у тебя предпочитаемый пол?", reply_markup=await get_prefer_gender_keyboard())
    
@dp.message(Registration.prefer_gender)
async def process_prefer_gender(message: Message, state: FSMContext) -> None:
    if message.text not in ["Мужской", "Женский", "Неважно"]:
        await message.answer("⚠️ Пожалуйста, выбери валидный пол.")
        return
    await state.update_data(prefer_gender=message.text)
    data = await state.get_data()
    await message.answer("Отлично! Теперь я знаю о тебе все! 🎉", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await create_user(data, message.from_user.id)
    
@dp.message(F.text == "Моя анкета")
async def my_profile(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        try:
            # --- 1. Получаем данные пользователя ---
            async with session.get(
                f"{API_URL}/users/{telegram_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 200:
                    await message.answer("Привет! Я тебя не нашёл в базе. Давай зарегистрируемся ✨")
                    await state.set_state(Registration.name)
                    await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))
                    return

                data = await resp.json()
                caption = (
                    f"{html.bold(data['name'])}, {html.bold(str(data['age']))}, "
                    f"{html.bold(data['city'])}\n\n{html.bold(data['description'] or 'Без описания')}"
                )

            # --- 2. Получаем фото пользователя ---
            async with session.get(
                f"{API_URL}/users/{telegram_id}/photos",
                headers={"x-api-key": API_KEY}
            ) as photo_resp:
                if photo_resp.status == 200:
                    photos_data = await photo_resp.json()
                    photos = photos_data.get("photos", [])

                    if photos:
                        media = []
                        tmp_files = []  # сохраняем, чтобы потом удалить

                        for i, p in enumerate(photos):
                            async with session.get("http://localhost:8000" + p["url"]) as resp:
                                if resp.status == 200:
                                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                                    tmp_file.write(await resp.read())
                                    tmp_file.close()

                                    # caption добавляем только к первому фото
                                    if i == 0:
                                        media.append(InputMediaPhoto(
                                            media=FSInputFile(tmp_file.name),
                                            caption=caption,
                                            parse_mode="HTML"
                                        ))
                                    else:
                                        media.append(InputMediaPhoto(media=FSInputFile(tmp_file.name)))

                                    tmp_files.append(tmp_file.name)

                        if media:
                            await message.answer_media_group(media)
                            await message.answer("⬆️ Вот твоя анкета", reply_markup=main_kb)

                        # удаляем файлы после отправки
                        for f in tmp_files:
                            os.remove(f)

                    else:
                        await message.answer(caption, reply_markup=main_kb)
                else:
                    await message.answer(caption, reply_markup=main_kb)

        except Exception as e:
            await message.answer("⚠️ Ошибка при соединении с сервером.")
            logging.error(f"API error: {e}")
    
@dp.message(F.text == "фото")
async def send_foto(message: Message):
    url = "http://127.0.0.1:8000/uploads/0a6fe7fb-ec1d-40b2-acb3-a24b7113e8be_%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202025-07-31%2013-31-47.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                # временно сохраняем файл
                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file.write(await resp.read())
                tmp_file.close()

                # отправляем в Telegram
                await message.answer_photo(FSInputFile(tmp_file.name))

                # удаляем временный файл
                os.remove(tmp_file.name)
            else:
                await message.answer("⚠️ Не удалось загрузить фото")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())