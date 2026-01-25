from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    age = State()
    city = State()
    description = State()
    gender = State()
    prefer_gender = State()
    photos = State()
    update = State()
