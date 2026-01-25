from aiogram.fsm.state import State, StatesGroup


class UpdateDescription(StatesGroup):
    description = State()
