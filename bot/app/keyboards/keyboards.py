from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def get_name_keyboard(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"{message.from_user.first_name}")  # type: ignore
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
    keyboard=[[KeyboardButton(text="Завершить")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profile_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
            KeyboardButton(text="5"),
            KeyboardButton(text="💤"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profile_with_likes_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔥"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
            KeyboardButton(text="5"),
            KeyboardButton(text="💤"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

swipe_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❤️"),
            KeyboardButton(text="👎"),
            KeyboardButton(text="💤"),
        ]
    ],
    resize_keyboard=True,
)


class MatchCb(CallbackData, prefix="profile"):
    candidate_id: int


def match_kb(candidate_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="🧠 Что написать?", callback_data=MatchCb(candidate_id=candidate_id).pack()
    )
    return kb.as_markup()
