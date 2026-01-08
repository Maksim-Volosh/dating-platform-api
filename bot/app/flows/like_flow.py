from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.like_presenter import LikePresenter
from app.services import InboxService, PhotoService, SwipeService, UserService
from app.states import LikeSwipeState


class LikeFlow:
    def __init__(
        self,
        user_service: UserService,
        photo_service: PhotoService,
        inbox_service: InboxService,
        swipe_service: SwipeService
    ):
        self.presenter = LikePresenter()
        self.user_service = user_service
        self.photo_service = photo_service
        self.inbox_service = inbox_service
        self.swipe_service = swipe_service

    async def next_like_profile(self, message: Message, state: FSMContext) -> None:
        if message.from_user:
            if message.text == "🔥":
                await self.presenter.start_swiping(message)

            inbox_data = await self.inbox_service.get_next_item(message.from_user.id)
            
            if inbox_data:
                candidate_id = inbox_data.get("candidate_id")
                type_of_inbox = inbox_data.get("type")

                more = await self.inbox_service.get_inbox_count(message.from_user.id)

                data = await self.user_service.get_user(candidate_id)
                
                if data:
                    photos = await self.photo_service.get_user_photos(data['telegram_id'])
                    
                    await state.update_data(current_profile_id=candidate_id)
                    await state.update_data(current_profile_name=data['name'])
                    
                    if not photos:
                        await self.presenter.send_profile_without_photos(message, data, more)
                    else:
                        await self.presenter.send_profile(message, data, photos, more)

                    if type_of_inbox == "MATCH":
                        await self.presenter.send_match(message, candidate_id, data['name'])
                        await self.inbox_service.ack_inbox_item(message.from_user.id, candidate_id)
                        await state.update_data(not_first_like=True)
                        await self.next_like_profile(message, state)
                        return
                    else:
                        await state.set_state(LikeSwipeState.swipe)
                else:
                    await self.presenter.send_error_getting_profile(message)
            else:
                state_data = await state.get_data()
                not_first_like = state_data.get("not_first_like", False)
                if message.text == "🔥" and not not_first_like:
                    await self.presenter.send_not_actual_data(message)
                else:
                    await self.presenter.send_no_more_profiles_today(message)
        
    async def swipe(self, message: Message, state: FSMContext, bot: Bot) -> None:
        data = await state.get_data()
        candidate_id = data.get("current_profile_id")
        name = data["current_profile_name"]
        if not name:
            name = "❤️"

        if message.from_user:
            if message.text == "❤️" and candidate_id:
                await state.clear()
                
                # --- Create swipe ---
                await self.presenter.send_match(message, candidate_id, name)
                await self.swipe_service.create_swipe(message.from_user.id, candidate_id, True)
                
                # --- Get count---
                count = await self.inbox_service.get_inbox_count(candidate_id)
                
                # --- Remove like ---
                await self.inbox_service.ack_inbox_item(message.from_user.id, candidate_id)
                
                # --- Send message to liked user ---
                await self.presenter.send_notification(count, candidate_id, bot)
                
                # --- Get next like profile ---
                await self.next_like_profile(message, state)
                
            elif message.text == "👎" and candidate_id:
                await state.clear()
                await self.swipe_service.create_swipe(message.from_user.id, candidate_id, False)
                await self.inbox_service.ack_inbox_item(message.from_user.id, candidate_id)
                await self.next_like_profile(message, state)