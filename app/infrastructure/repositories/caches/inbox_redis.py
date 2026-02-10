from redis.asyncio import Redis

from app.domain.interfaces import IInboxCache
from app.domain.entities import InboxItem, InboxItemType


class InboxRedisCache(IInboxCache):
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def add_incoming(self, owner_id: int, candidate_id: int, timeout=None):
        key_list = f"inbox:{owner_id}:list"
        set_key = f"inbox:{owner_id}:set"

        added = await self.client.sadd(set_key, candidate_id)  # type: ignore

        if added:
            await self.client.rpush(key_list, f"{candidate_id}:INCOMING")  # type: ignore
            if timeout:
                await self.client.expire(key_list, timeout)

        if timeout:
            await self.client.expire(set_key, timeout)

    async def add_match(self, owner_id: int, candidate_id: int, timeout=None):
        key_list = f"inbox:{owner_id}:list"
        set_key = f"inbox:{owner_id}:set"

        added = await self.client.sadd(set_key, candidate_id)  # type: ignore

        if added:
            await self.client.rpush(key_list, f"{candidate_id}:MATCH")  # type: ignore

        if timeout:
            await self.client.expire(key_list, timeout)
            await self.client.expire(set_key, timeout)

    async def peek(self, owner_id: int) -> InboxItem | None:
        key_list = f"inbox:{owner_id}:list"

        item = await self.client.lindex(key_list, 0)  # type: ignore

        if item:
            candidate_id, type_ = item.decode().split(":")  # type: ignore
            return InboxItem(candidate_id=int(candidate_id), type=InboxItemType(type_))
        return None

    async def ack(self, owner_id: int, candidate_id: int):
        key_list = f"inbox:{owner_id}:list"
        set_key = f"inbox:{owner_id}:set"

        await self.client.lrem(key_list, 1, f"{candidate_id}:INCOMING")  # type: ignore
        await self.client.lrem(key_list, 1, f"{candidate_id}:MATCH")  # type: ignore

        await self.client.srem(set_key, candidate_id)  # type: ignore

    async def count(self, owner_id: int):
        key_list = f"inbox:{owner_id}:list"
        return await self.client.llen(key_list)  # type: ignore
