from app.domain.entities.user import UserEntity
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)
from app.domain.interfaces import IUserRepository


class UserUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo
        
    async def get_by_id(self, telegram_id: int) -> UserEntity:
        user: UserEntity | None = await self.repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById()
        return user
    
    async def get_all(self) -> list[UserEntity]:
        users = await self.repo.get_all()
        if users is None:
            raise UsersNotFound
        return users
    
    async def create(self, user: UserEntity) -> UserEntity:
        created_user = await self.repo.create(user)
        if created_user is None:
            raise UserAlreadyExists
        return created_user
    
    async def update(self, telegram_id: int, update: UserEntity) -> UserEntity:
        updated_user = await self.repo.update(telegram_id, update)
        if updated_user is None:
            raise UserNotFoundById
        return updated_user