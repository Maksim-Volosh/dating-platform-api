from typing import List

from app.domain.entities import PhotoEntity, UserEntity
from app.domain.exceptions import (PhotosNotFound, TooManyPhotos)
from app.domain.interfaces import IPhotoRepository


class RetrieveUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository, 
    ) -> None:
        self.photo_repo = photo_repo
        
    async def execute(self, user: UserEntity) -> list[PhotoEntity]:
        photos: List[PhotoEntity] | None = await self.photo_repo.get_by_user_id(user.telegram_id)
        if photos is None:
            raise PhotosNotFound
        return photos
    

class UpdateUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository
    ) -> None:
        self.photo_repo = photo_repo
    
    async def execute(
        self, user: UserEntity, photos: List[PhotoEntity]
    ) -> List[PhotoEntity]:
        # Delete old photos
        deleted_photos: List[PhotoEntity] | None = await self.photo_repo.delete(user.telegram_id)
        
        # Validate new photos
        if len(photos) > 3:
            raise TooManyPhotos(
                f"User can have a maximum of 3 photos. You can upload 3 more photos at this time."
            )
            
        # Save new photos to database
        file_ids: List[PhotoEntity] = await self.photo_repo.create(user.telegram_id, photos) 
        return file_ids
        

class UploadUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository
    ) -> None:
        self.photo_repo = photo_repo
    
    async def execute(
        self, user: UserEntity, photos: List[PhotoEntity]
    ) -> List[PhotoEntity]:
        user_photos = await self.photo_repo.get_by_user_id(user.telegram_id)
        if user_photos is None:
            photos_len = 0
        else:
            photos_len = len(user_photos)
        
        if photos_len >= 3:
            raise TooManyPhotos("User already has 3 photos")
        elif photos_len + len(photos) > 3:
            raise TooManyPhotos(
                f"User can have a maximum of 3 photos. You can upload {3 - photos_len} more photo(s) at this time."
            )
            
        file_ids: List[PhotoEntity] = await self.photo_repo.create(user.telegram_id, photos) 
        return file_ids


class DeleteUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository
    ) -> None:
        self.photo_repo = photo_repo
    
    async def execute(
        self, user: UserEntity
    ) -> None:
        deleted_photos: List[PhotoEntity] | None = await self.photo_repo.delete(user.telegram_id)
        if deleted_photos is None:
            raise PhotosNotFound
        
        return