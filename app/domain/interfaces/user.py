from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, telegram_id: int) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[UserEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, telegram_id: int, update: UserEntity) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_description(
        self, telegram_id: int, description: str
    ) -> UserEntity | None:
        raise NotImplementedError

    # @abstractmethod
    # async def delete(self, user: UserEntity) -> UserEntity:
    #     raise NotImplementedError
