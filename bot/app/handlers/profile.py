from aiogram import Dispatcher, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.container import container
from app.flows.profile_flow import ProfileFlow
from app.states import LikeSwipeState, SwipeState

router = Router()
flow = ProfileFlow(container.user_service, container.photo_service)

@router.message(
    StateFilter(None, SwipeState.swipe, LikeSwipeState.swipe), 
    F.text.in_({"💤", "Моя анкета"})
)
async def my_profile(message: Message, state: FSMContext) -> None:
    await flow.show_my_profile(message, state)
    
    
def register(dp: Dispatcher) -> None:
    dp.include_router(router)