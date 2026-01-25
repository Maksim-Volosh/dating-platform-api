from aiogram.fsm.state import State, StatesGroup


class UpdatePhotos(StatesGroup):
    photos = State()
