from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.api.v1.schemas.photo import PhotoResponse, PhotoURL
from app.core.containers.photo import (get_delete_user_photos_use_case,
                                       get_retrieve_user_photos_use_case,
                                       get_update_user_photos_use_case,
                                       get_upload_user_photos_use_case)
from app.domain.exceptions import (PhotosNotFound, TooManyPhotos,
                                   UserNotFoundById, WrongFileExtension)
from app.domain.use_cases import (DeleteUserPhotosUseCase,
                                  RetrieveUserPhotosUseCase,
                                  UpdateUserPhotosUseCase,
                                  UploadUserPhotosUseCase)
from app.infrastructure.mappers.photo_mapper import to_entities

router = APIRouter(prefix="/users", tags=["User Photos"])


@router.get("/{telegram_id}/photos", status_code=200)
async def get_user_photos(
    telegram_id: int,
    use_case: RetrieveUserPhotosUseCase = Depends(get_retrieve_user_photos_use_case)
) -> PhotoResponse:
    try:
        photos = await use_case.execute(telegram_id)
    except UserNotFoundById as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    except PhotosNotFound as e:
        raise HTTPException(
            status_code=404, detail=e.message
        )
    
    return PhotoResponse(
        user_id=telegram_id, 
        photos=[PhotoURL.model_validate(photo, from_attributes=True) for photo in photos]
    )
    
@router.delete("/{telegram_id}/photos", status_code=204)
async def delete_user_photos(
    telegram_id: int,
    use_case: DeleteUserPhotosUseCase = Depends(get_delete_user_photos_use_case)
):
    try:
        await use_case.execute(telegram_id)
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
    telegram_id: int,
    photos: List[UploadFile],
    use_case: UploadUserPhotosUseCase = Depends(get_upload_user_photos_use_case)
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_urls = await use_case.execute(telegram_id, photo_entities)
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
        user_id=telegram_id, 
        photos=[PhotoURL.model_validate(photo, from_attributes=True) for photo in photo_urls]
    )
    
@router.put("/{telegram_id}/photos", status_code=201)
async def update_user_photos(
    telegram_id: int,
    photos: List[UploadFile],
    use_case: UpdateUserPhotosUseCase = Depends(get_update_user_photos_use_case)
) -> PhotoResponse:
    photo_entities = await to_entities(photos)
    try:
        photo_urls = await use_case.execute(telegram_id=telegram_id, photos=photo_entities)
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
        user_id=telegram_id,
        photos=[PhotoURL(url=p.url) for p in photo_urls]
    )