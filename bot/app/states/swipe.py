from aiogram.fsm.state import State, StatesGroup


class SwipeState(StatesGroup):
    swipe = State()