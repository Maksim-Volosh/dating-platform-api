from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.container import container
from app.flows.like_flow import LikeFlow
from app.states import LikeSwipeState

router = Router()
flow = LikeFlow(container.user_service, container.photo_service, container.inbox_service)

@router.message(StateFilter(None), F.text == "🔥")
async def next_like_profile(message: Message, state: FSMContext) -> None:
    await flow.next_like_profile(message, state)

@router.message(LikeSwipeState.swipe)
async def swipe(message: Message, state: FSMContext, bot: Bot) -> None:
    await flow.swipe(message, state, bot)


def register(dp: Dispatcher) -> None:
    dp.include_router(router)