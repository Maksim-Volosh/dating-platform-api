import json
from typing import List

from redis import Redis

from app.domain.entities import UserEntity
from app.domain.interfaces import IDeckCache


class DeckRedisCache(IDeckCache):
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def rpush(self, key: str, users: List[UserEntity], timeout=None):
        users_dict = [user.to_dict() for user in users]
        users_json = [json.dumps(user) for user in users_dict]
        await self.client.rpush(key, *users_json)  # type: ignore
        if timeout:
            await self.client.expire(key, timeout)

    async def lpop(self, key: str) -> UserEntity | None:
        user_json = await self.client.lpop(key)  # type: ignore
        if not user_json:
            return None
        if type(user_json) == bytes or type(user_json) == str:
            return UserEntity(**json.loads(user_json))
        else:
            return None

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def get_deck(self, key: str) -> List[UserEntity] | None:
        data = await self.client.lrange(key, 0, -1)  # type: ignore

        if not data:
            return None

        parsed = [json.loads(item) for item in data]

        return [UserEntity(**item) for item in parsed]
