from aiogram import Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.container import container
from app.flows.ai import AIFlow
from app.keyboards.keyboards import MatchCb

router = Router()
flow = AIFlow(container.ai_service)


@router.message(
    StateFilter(None),
    F.text == "5",
)
async def ai_profile_analyze(message: Message, state: FSMContext) -> None:
    await flow.ai_profile_analyze(message, state)


@router.callback_query(MatchCb.filter())
async def ai_match_opener(
    call: CallbackQuery, callback_data: MatchCb, state: FSMContext
):
    await flow.ai_match_opener(call, callback_data, state)


def register(dp: Dispatcher) -> None:
    dp.include_router(router)
