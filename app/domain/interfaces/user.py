from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import UserEntity


class IUserRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    @abstractmethod
    async def get_by_id(self, telegram_id: int) -> UserEntity | None:
        raise NotImplementedError
        
    @abstractmethod
    async def get_all(self) -> list[UserEntity] | None:
        raise NotImplementedError
    
    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity | None:
        raise NotImplementedError
        
    @abstractmethod
    async def update(self, telegram_id: int, update: UserEntity) -> UserEntity | None:
        raise NotImplementedError
        
    # @abstractmethod
    # async def delete(self, user: UserEntity) -> UserEntity:
    #     raise NotImplementedError