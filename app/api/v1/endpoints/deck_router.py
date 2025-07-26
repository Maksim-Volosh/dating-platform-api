import json

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.user_schemas import UserResponse
from app.infrastructure.db import db_helper
from app.infrastructure.models.users import User
from app.infrastructure.redis import redis_helper

router = APIRouter(prefix="/decks", tags=["Deck"])

class DeckService:
    def __init__(self, db: AsyncSession, redis: redis.Redis) -> None:
        self.db = db
        self.redis = redis

    async def build_deck(self, telegram_id: int) -> None:
        user: User | None = await self.db.get(User, telegram_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_age = user.age
        user_gender = user.gender
        user_city = user.city
        
        prefer_gender = user.prefer_gender
        prefer_ages = list(range(user_age - 2, user_age + 3))
        
        if prefer_gender != 'anyone':
            q = select(User).where(
                User.city == user_city,
                User.age.in_(prefer_ages),
                User.gender == prefer_gender,
                User.prefer_gender.in_(['anyone', user_gender])
            )
        else:
            q = select(User).where(
                User.city == user_city,
                User.age.in_(prefer_ages),
                User.prefer_gender.in_(['anyone', user_gender])
            )
            
        result = await self.db.execute(q)
        users_models = result.scalars().all()
        users_pydantic = [UserResponse.model_validate(user, from_attributes=True) for user in users_models]
        users_json = [json.dumps(jsonable_encoder(user)) for user in users_pydantic]
        
        await self.redis.rpush(f"deck:{telegram_id}", *users_json) # type: ignore
        await self.redis.expire(f"deck:{telegram_id}", 60*60*2)
        
    async def get_next_user(self, telegram_id: int) -> UserResponse | None:
        user_bytes = await self.redis.lpop(f"deck:{telegram_id}") # type: ignore
        if not user_bytes or not type(user_bytes) == bytes:
            await self.build_deck(telegram_id)
            user_bytes = await self.redis.lpop(f"deck:{telegram_id}") # type: ignore
            
            if not user_bytes or not type(user_bytes) == bytes:   
                return None
        user_pydantic = UserResponse(**json.loads(user_bytes))
        return user_pydantic

    
@router.get("/{telegram_id}")
async def get_next_user_from_deck(
    telegram_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    redis: redis.Redis = Depends(redis_helper.get_client)
) -> UserResponse:
    deck_service = DeckService(db, redis)
    user: UserResponse | None = await deck_service.get_next_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="No more users in the deck")
    return user