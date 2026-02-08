from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.schemas.user import (
    UserCreateRequest,
    UserCreateResponse,
    UserResponse,
    UserUpdateDescriptionRequest,
    UserUpdateRequest,
    UserUpdateResponse,
    UserDistanceResponse,
)
from app.core.composition.container import Container
from app.core.composition.di import get_container
from app.domain.entities import UserEntity
from app.domain.exceptions import UserAlreadyExists, UserNotFoundById, UsersNotFound

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/{telegram_id}")
async def get_user(
    telegram_id: int, container: Container = Depends(get_container)
) -> UserResponse:
    try:
        user = await container.user_use_case().get_by_id(telegram_id=telegram_id)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    return UserResponse.model_validate(user, from_attributes=True)


@router.get("/{telegram_id}/profile")
async def get_user_profile_view(
    telegram_id: int,
    viewer_id: int = Query(..., description="Who is viewing the profile"),
    container: Container = Depends(get_container),
) -> UserDistanceResponse:
    try:
        user = await container.get_user_profile_view_use_case().execute(
            candidate_id=telegram_id, viewer_id=viewer_id
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    return UserDistanceResponse.model_validate(user, from_attributes=True)


@router.get("/")
async def get_users(
    container: Container = Depends(get_container),
) -> List[UserResponse]:
    try:
        users = await container.user_use_case().get_all()
    except UsersNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return [UserResponse.model_validate(user, from_attributes=True) for user in users]


@router.post("/", status_code=201)
async def create_user(
    user: UserCreateRequest, container: Container = Depends(get_container)
) -> UserCreateResponse:
    user_entity = user.to_entity()
    try:
        new_user: UserEntity = await container.create_user_use_case().execute(
            user_entity
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    return UserCreateResponse.model_validate(new_user, from_attributes=True)


@router.put("/{telegram_id}")
async def update_user(
    telegram_id: int,
    update: UserUpdateRequest,
    container: Container = Depends(get_container),
) -> UserUpdateResponse:
    update_entity = update.to_entity()
    try:
        user_model = await container.update_user_use_case().execute(
            telegram_id, update_entity
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    return UserUpdateResponse.model_validate(user_model, from_attributes=True)


@router.patch("/{telegram_id}/description")
async def update_user_description(
    telegram_id: int,
    update: UserUpdateDescriptionRequest,
    container: Container = Depends(get_container),
) -> UserUpdateResponse:
    try:
        user_model = await container.update_user_description_use_case().execute(
            telegram_id, update.description
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    return UserUpdateResponse.model_validate(user_model, from_attributes=True)
