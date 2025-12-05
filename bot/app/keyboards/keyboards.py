
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_name_keyboard(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"{message.from_user.first_name}") # type: ignore
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

photo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Завершить")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profile_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)