from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.user import (UserCreateRequest, UserCreateResponse,
                                     UserResponse, UserUpdateRequest,
                                     UserUpdateResponse)
from app.core.containers.user import get_user_use_case
from app.domain.entities import UserEntity
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)
from app.domain.use_cases import UserUseCase

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/{telegram_id}")
async def get_user(  
    telegram_id: int,  
    use_case: UserUseCase = Depends(get_user_use_case)
) -> UserResponse:
    try:
        user = await use_case.get_by_id(telegram_id=telegram_id)
    except UserNotFoundById:
        raise HTTPException(status_code=404, detail=f"User with Id: {telegram_id} not found")
    return UserResponse.model_validate(user, from_attributes=True)

@router.get("/")
async def get_users(    
    use_case: UserUseCase = Depends(get_user_use_case)
) -> List[UserResponse]:
    try:
        users = await use_case.get_all()
    except UsersNotFound:
        raise HTTPException(status_code=404, detail="No users found")
    return [UserResponse.model_validate(user, from_attributes=True) for user in users]

@router.post("/")
async def create_user(
    user: UserCreateRequest,
    use_case: UserUseCase = Depends(get_user_use_case)
) -> UserCreateResponse:
    user_entity = user.to_entity()
    try:
        new_user: UserEntity = await use_case.create(user_entity)
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="User with this Telegram ID already exists")
    return UserCreateResponse.model_validate(new_user, from_attributes=True)

@router.put("/{telegram_id}")
async def update_user(  
    telegram_id: int,  
    update: UserUpdateRequest,
    use_case: UserUseCase = Depends(get_user_use_case)
) -> UserUpdateResponse:
    update_entity = update.to_entity()
    try:
        user_model = await use_case.update(telegram_id, update_entity)
    except UserNotFoundById:
        raise HTTPException(status_code=404, detail=f"User with Id: {telegram_id} not found")
    return UserUpdateResponse.model_validate(user_model, from_attributes=True)


