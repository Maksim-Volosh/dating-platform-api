from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.flows.swipe_flow import SwipeFlow
from app.states import SwipeState

router = Router()
flow = SwipeFlow()

@router.message(StateFilter(None), F.text.in_({"1", "Листать анкеты"}))
async def next_profile(message: Message, state: FSMContext) -> None:
    await flow.next_profile(message, state)

@router.message(SwipeState.swipe)
async def swipe(message: Message, state: FSMContext, bot: Bot) -> None:
    await flow.swipe(message, state, bot)


def register(dp: Dispatcher) -> None:
    dp.include_router(router)