from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.photo import PhotoFileId, PhotoResponse
from app.core.container import Container
from app.core.dependencies import get_existing_user
from app.core.di import get_container
from app.domain.entities import UserEntity
from app.domain.entities.photo import PhotoEntity
from app.domain.exceptions import (
    PhotosNotFound,
    TooManyPhotos,
    UserNotFoundById,
    WrongFileExtension,
)
from app.infrastructure.mappers.photo_mapper import to_entities

router = APIRouter(prefix="/users", tags=["User Photos"])


@router.get("/{telegram_id}/photos", status_code=200)
async def get_user_photos(
    user: UserEntity = Depends(get_existing_user),
    container: Container = Depends(get_container),
) -> PhotoResponse:
    try:
        photos: List[PhotoEntity] = (
            await container.retrieve_user_photos_use_case().execute(user)
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PhotosNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)

    return PhotoResponse(
        user_id=user.telegram_id,
        photos=[
            PhotoFileId.model_validate(photo, from_attributes=True) for photo in photos
        ],
    )


@router.delete("/{telegram_id}/photos", status_code=204)
async def delete_user_photos(
    user: UserEntity = Depends(get_existing_user),
    container: Container = Depends(get_container),
):
    try:
        await container.delete_user_photos_use_case().execute(user)
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PhotosNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return


@router.post("/{telegram_id}/photos", status_code=201)
async def upload_user_photos(
    photos: List[PhotoFileId],
    user: UserEntity = Depends(get_existing_user),
    container: Container = Depends(get_container),
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_urls = await container.upload_user_photos_use_case().execute(
            user, photo_entities
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except TooManyPhotos as e:
        raise HTTPException(status_code=400, detail=e.message)
    except WrongFileExtension as e:
        raise HTTPException(status_code=400, detail=e.message)

    return PhotoResponse(
        user_id=user.telegram_id,
        photos=[
            PhotoFileId.model_validate(photo, from_attributes=True)
            for photo in photo_urls
        ],
    )


@router.put("/{telegram_id}/photos", status_code=201)
async def update_user_photos(
    photos: List[PhotoFileId],
    user: UserEntity = Depends(get_existing_user),
    container: Container = Depends(get_container),
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_file_ids = await container.update_user_photos_use_case().execute(
            user, photo_entities
        )
    except UserNotFoundById as e:
        raise HTTPException(status_code=404, detail=e.message)
    except TooManyPhotos as e:
        raise HTTPException(status_code=400, detail=e.message)
    except WrongFileExtension as e:
        raise HTTPException(status_code=400, detail=e.message)

    return PhotoResponse(
        user_id=user.telegram_id,
        photos=[PhotoFileId(file_id=p.file_id) for p in photo_file_ids],
    )
