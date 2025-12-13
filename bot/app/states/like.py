from aiogram.fsm.state import State, StatesGroup


class LikeSwipeState(StatesGroup):
    swipe = State()