from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.photo import PhotoFileId, PhotoResponse
from app.core.containers.photo import (get_delete_user_photos_use_case,
                                       get_retrieve_user_photos_use_case,
                                       get_update_user_photos_use_case,
                                       get_upload_user_photos_use_case)
from app.core.dependencies import get_existing_user
from app.domain.entities import UserEntity
from app.domain.entities.photo import PhotoEntity
from app.domain.exceptions import (PhotosNotFound, TooManyPhotos,
                                   UserNotFoundById, WrongFileExtension)
from app.application.use_cases import (DeleteUserPhotosUseCase,
                                  RetrieveUserPhotosUseCase,
                                  UpdateUserPhotosUseCase,
                                  UploadUserPhotosUseCase)
from app.infrastructure.mappers.photo_mapper import to_entities

router = APIRouter(prefix="/users", tags=["User Photos"])


@router.get("/{telegram_id}/photos", status_code=200)
async def get_user_photos(
    user: UserEntity = Depends(get_existing_user),
    use_case: RetrieveUserPhotosUseCase = Depends(get_retrieve_user_photos_use_case)
) -> PhotoResponse:
    try:
        photos: List[PhotoEntity] = await use_case.execute(user)
    except UserNotFoundById as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    except PhotosNotFound as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    
    return PhotoResponse(
        user_id=user.telegram_id, 
        photos=[PhotoFileId.model_validate(photo, from_attributes=True) for photo in photos]
    )
    
@router.delete("/{telegram_id}/photos", status_code=204)
async def delete_user_photos(
    user: UserEntity = Depends(get_existing_user),
    use_case: DeleteUserPhotosUseCase = Depends(get_delete_user_photos_use_case)
):
    try:
        await use_case.execute(user)
    except UserNotFoundById as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    except PhotosNotFound as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    return
    
@router.post("/{telegram_id}/photos", status_code=201)
async def upload_user_photos(
    photos: List[PhotoFileId],
    user: UserEntity = Depends(get_existing_user),
    use_case: UploadUserPhotosUseCase = Depends(get_upload_user_photos_use_case)
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_urls = await use_case.execute(user, photo_entities)
    except UserNotFoundById as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    except TooManyPhotos as e:
        raise HTTPException(status_code=400, detail=e.message)
    except WrongFileExtension as e:
        raise HTTPException(
            status_code=400, detail=e.message
        )
    
    return PhotoResponse(
        user_id=user.telegram_id, 
        photos=[PhotoFileId.model_validate(photo, from_attributes=True) for photo in photo_urls]
    )
    
@router.put("/{telegram_id}/photos", status_code=201)
async def update_user_photos(
    photos: List[PhotoFileId],
    user: UserEntity = Depends(get_existing_user),
    use_case: UpdateUserPhotosUseCase = Depends(get_update_user_photos_use_case)
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_file_ids = await use_case.execute(user, photo_entities)
    except UserNotFoundById as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    except TooManyPhotos as e:
        raise HTTPException(status_code=400, detail=e.message)
    except WrongFileExtension as e:
        raise HTTPException(
            status_code=400, detail=e.message
        )
    
    return PhotoResponse(
        user_id=user.telegram_id,
        photos=[PhotoFileId(file_id=p.file_id) for p in photo_file_ids]
    )