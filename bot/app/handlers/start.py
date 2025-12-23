from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.flows.start_flow import StartFlow

router = Router()
flow = StartFlow()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await flow.start(message, state)
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)