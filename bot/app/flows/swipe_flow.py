from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.presenters.swipe_presenter import SwipePresenter
from app.services import DeckService, InboxService, PhotoService, SwipeService
from app.states import SwipeState
from app.states.swipe import SwipeState


class SwipeFlow:
    def __init__(
        self,
        photo_service: PhotoService,
        inbox_service: InboxService,
        swipe_service: SwipeService,
        deck_service: DeckService
    ):
        self.photo_service = photo_service
        self.presenter = SwipePresenter()
        self.inbox_service = inbox_service
        self.swipe_service = swipe_service
        self.deck_service = deck_service

    async def next_profile(self, message: Message, state: FSMContext) -> None:
        if message.text in ["1", "Листать анкеты"]:
            await self.presenter.start_swiping(message)
        
        if message.from_user:
            # --- 1. Get user data ---
            data = await self.deck_service.get_next_user(message.from_user.id)
            
            if data:
                # --- 2. Get user photos ---
                photos = await self.photo_service.get_user_photos(data['telegram_id'])
                
                await state.update_data(current_profile_id=data['telegram_id'])
                if not photos:
                    await self.presenter.send_profile_without_photos(message, data)
                    await state.set_state(SwipeState.swipe)
                    return

                await self.presenter.send_profile(message, data, photos)
                await state.set_state(SwipeState.swipe)
            else:
                await self.presenter.send_no_more_profiles(message)
            
        
    async def swipe(self, message: Message, state: FSMContext, bot: Bot) -> None:
        data = await state.get_data()
        liked_id = data.get("current_profile_id")

        if message.from_user:
            if message.text == "❤️" and liked_id:
                
                # --- Create swipe ---
                await self.swipe_service.create_swipe(message.from_user.id, liked_id, True)
                await self.presenter.send_successful_swipe(message)
                
                # --- Get count---
                count = await self.inbox_service.get_inbox_count(liked_id)
                
                # --- Send message to liked user ---
                await self.presenter.send_notification(count, liked_id, bot)
                
                # --- Get next profile ---
                await state.clear()
                await self.next_profile(message, state)
                
            elif message.text == "👎" and liked_id:
                await state.clear()
                await self.swipe_service.create_swipe(message.from_user.id, liked_id, False)
                await self.next_profile(message, state)