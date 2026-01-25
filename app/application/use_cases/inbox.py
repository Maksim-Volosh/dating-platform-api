from app.domain.interfaces import IInboxCache
from app.domain.exceptions import InboxItemNotFound
from app.domain.entities import InboxItem


class InboxUseCase:
    def __init__(self, cache: IInboxCache) -> None:
        self.cache = cache

    async def peek_current(self, owner_id: int) -> InboxItem:
        item = await self.cache.peek(owner_id)

        if item is None:
            raise InboxItemNotFound()

        return item

    async def get_count(self, liked_id: int) -> int:
        count = await self.cache.count(liked_id)
        return count

    async def ack_item(self, owner_id: int, candidate_id: int):
        await self.cache.ack(owner_id, candidate_id)
