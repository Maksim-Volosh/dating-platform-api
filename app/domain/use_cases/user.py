from app.domain.entities import UserEntity
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)
from app.domain.interfaces import IUserRepository
from app.domain.services import DeckBuilderService


class UserUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo
        
    async def get_by_id(self, telegram_id: int) -> UserEntity:
        user: UserEntity | None = await self.repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        return user
    
    async def get_all(self) -> list[UserEntity]:
        users = await self.repo.get_all()
        if users is None:
            raise UsersNotFound
        return users
    
    async def update(self, telegram_id: int, update: UserEntity) -> UserEntity:
        updated_user = await self.repo.update(telegram_id, update)
        if updated_user is None:
            raise UserNotFoundById
        return updated_user
    
class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository, deck_builder: DeckBuilderService) -> None:
        self.user_repo = user_repo
        self.deck_builder = deck_builder
        
    async def execute(self, user: UserEntity) -> UserEntity:
        created_user = await self.user_repo.create(user)
        if created_user is None:
            raise UserAlreadyExists
        
        if created_user:
            await self.deck_builder.build(created_user)
            
        return created_user