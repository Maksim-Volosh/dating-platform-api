from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import UserEntity
from app.domain.interfaces import IUserRepository
from app.infrastructure.mappers import UserMapper
from app.infrastructure.models import User


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session):
        self.session: AsyncSession = session
        
    async def get_by_id(self, telegram_id) -> UserEntity | None:
        user_model = await self.session.get(User, telegram_id)
        if user_model is None:
            return None
        return UserMapper.to_entity(user_model)
        
    async def get_all(self) -> List[UserEntity] | None:
        q = select(User)
        result = await self.session.execute(q)
        user_models = result.scalars().all()
        
        if user_models is None:
            return None

        return [UserMapper.to_entity(user_model) for user_model in user_models]
    
    async def create(self, user: UserEntity) -> UserEntity | None:
        new_user = UserMapper.to_model(user)
        self.session.add(new_user)
        
        try:
            await self.session.flush()
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig):
                await self.session.rollback()
                return None
            else:
                raise
        await self.session.commit()
        return UserMapper.to_entity(new_user)
    
    async def update(self, telegram_id: int, update: UserEntity) -> UserEntity | None:
        user_model = await self.session.get(User, telegram_id)
        if user_model is None:
            return None
        
        for field, value in update.__dict__.items():
            if field != "telegram_id":
                setattr(user_model, field, value)
            
        await self.session.commit()
        return UserMapper.to_entity(user_model)
    
    async def update_description(self, telegram_id: int, description: str) -> UserEntity | None:
        user_model = await self.session.get(User, telegram_id)
        if user_model is None:
            return None
        
        user_model.description = description
        await self.session.commit()
        return UserMapper.to_entity(user_model)
