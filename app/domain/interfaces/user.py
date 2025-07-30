from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import UserEntity


class IUserRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
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
    async def get_users_by_preferences(self, city: str, age: int, gender: str, prefer_gender: str) -> List[UserEntity] | None:
        raise NotImplementedError
        
    # @abstractmethod
    # async def delete(self, user: UserEntity) -> UserEntity:
    #     raise NotImplementedError