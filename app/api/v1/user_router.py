import select
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.v1.schemas.user_schemas import (UserCreateRequest,
                                             UserCreateResponse,
                                             UserReadResponse, UserUpdateRequest, UserUpdateResponse)
from app.infrastructure.db import db_helper
from app.infrastructure.models.users import User

router = APIRouter()


@router.get("/")
async def get_users(    
    db: AsyncSession = Depends(db_helper.session_getter)
) -> List[UserReadResponse]:
    q = select(User)
    result = await db.execute(q)
    user_models = result.scalars().all()

    return [UserReadResponse.model_validate(user, from_attributes=True) for user in user_models]

@router.get("/{user_id}")
async def get_user(  
    user_id: int,  
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UserReadResponse:
    user_model = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User with Id: {user_id} not found")

    return UserReadResponse.model_validate(user_model, from_attributes=True)

@router.post("/")
async def create_user(
    user: UserCreateRequest,
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UserCreateResponse:
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.flush()
    await db.commit()
    return UserCreateResponse.model_validate(new_user, from_attributes=True)

@router.put("/{user_id}")
async def update_user(  
    user_id: int,  
    update: UserUpdateRequest,
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UserUpdateResponse:
    user_model = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User with Id: {user_id} not found")
    
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(user_model, field, value)
        
    await db.commit()
    return UserUpdateResponse.model_validate(user_model, from_attributes=True)


