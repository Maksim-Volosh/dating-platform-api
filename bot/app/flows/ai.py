from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.container import container
from app.keyboards.keyboards import MatchCb
from app.presenters.ai_presenter import AIPresenter
from app.services import AIService
from app.states import AIState


class AIFlow:
    def __init__(self, ai_service: AIService):
        self.presenter = AIPresenter()
        self.ai_service = ai_service

    async def ai_profile_analyze(self, message: Message, state: FSMContext) -> None:
        if message.from_user:
            await state.set_state(AIState.ai)
            await self.presenter.send_wait(message)
            result = await self.ai_service.get_ai_profile_analyze(message.from_user.id)
            if result is None:
                await self.presenter.send_error(message)
            elif result is False:
                await self.presenter.send_limit(message)
            else:
                await self.presenter.send_result(message, result)
            await state.clear()

    async def ai_match_opener(
        self, call: CallbackQuery, callback_data: MatchCb, state: FSMContext
    ) -> None:
        await call.answer()
        if call.bot:
            await self.presenter.send_call_wait(call.bot, call.from_user.id)

            result = await container.ai_service.get_ai_match_opener(
                candidate_id=callback_data.candidate_id,
                liker_id=call.from_user.id,
            )

            if result is None:
                await self.presenter.send_call_error(call.bot, call.from_user.id)
            elif result is False:
                await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text="За сегодня слишком много запросов. Попробуй позже :)",
                )
            else:
                await self.presenter.send_call_result(
                    call.bot, call.from_user.id, result
                )
