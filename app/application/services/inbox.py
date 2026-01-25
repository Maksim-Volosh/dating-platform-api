from app.domain.interfaces import IInboxCache
from app.domain.entities import InboxSwipe
from app.core.config import settings


class InboxOnSwipeService:
    def __init__(self, inbox_cache: IInboxCache) -> None:
        self.inbox_cache = inbox_cache

    async def _is_match(self, swipe: InboxSwipe) -> bool:
        if swipe.to_user_id_decision is True:
            return True
        else:
            return False

    async def create_inbox_item(self, swipe: InboxSwipe):
        if await self._is_match(swipe):
            await self.inbox_cache.add_match(
                swipe.to_user_id, swipe.from_user_id, timeout=settings.inbox.timeout
            )
        else:
            await self.inbox_cache.add_incoming(
                swipe.to_user_id, swipe.from_user_id, timeout=settings.inbox.timeout
            )
