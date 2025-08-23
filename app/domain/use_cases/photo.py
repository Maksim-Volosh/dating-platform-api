from typing import List

from app.domain.entities import (PhotoEntity, PhotoUniqueNameEntity,
                                 PhotoUrlEntity, UserEntity)
from app.domain.exceptions import (PhotosNotFound, TooManyPhotos,
                                   WrongFileExtension)
from app.domain.interfaces import IPhotoRepository, IPhotoStorage


class RetrieveUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository, 
    ) -> None:
        self.photo_repo = photo_repo
        
    async def execute(self, user: UserEntity) -> list[PhotoUrlEntity]:
        photos: List[PhotoUrlEntity] | None = await self.photo_repo.get_by_user_id(user.telegram_id)
        if photos is None:
            raise PhotosNotFound
        return photos
    

class UpdateUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository, 
        file_storage: IPhotoStorage
    ) -> None:
        self.photo_repo = photo_repo
        self.file_storage = file_storage
    
    async def execute(
        self, user: UserEntity, photos: List[PhotoEntity]
    ) -> List[PhotoUrlEntity]:
        # Delete old photos
        deleted_photos: List[PhotoUrlEntity] | None = await self.photo_repo.delete(user.telegram_id)
        if deleted_photos:
            await self.file_storage.delete(deleted_photos)
        
        # Validate new photos
        if len(photos) > 3:
            raise TooManyPhotos(
                f"User can have a maximum of 3 photos. You can upload 3 more photos at this time."
            )
        
        # Save new photos to local storage
        unique_names: List[PhotoUniqueNameEntity] | None = await self.file_storage.save(files=photos)
        if unique_names is None:
            raise WrongFileExtension
            
        # Save new photos to database
        urls: List[PhotoUrlEntity] = await self.photo_repo.create(user.telegram_id, unique_names) 
        return urls
        

class UploadUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository, 
        file_storage: IPhotoStorage
    ) -> None:
        self.photo_repo = photo_repo
        self.file_storage = file_storage
    
    async def execute(
        self, user: UserEntity, photos: List[PhotoEntity]
    ) -> List[PhotoUrlEntity]:
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
        
        unique_names: List[PhotoUniqueNameEntity] | None = await self.file_storage.save(files=photos)
        if unique_names is None:
            raise WrongFileExtension
            
        urls: List[PhotoUrlEntity] = await self.photo_repo.create(user.telegram_id, unique_names) 
        return urls


class DeleteUserPhotosUseCase:
    def __init__(
        self,
        photo_repo: IPhotoRepository, 
        file_storage: IPhotoStorage
    ) -> None:
        self.photo_repo = photo_repo
        self.file_storage = file_storage
    
    async def execute(
        self, user: UserEntity
    ) -> None:
        deleted_photos: List[PhotoUrlEntity] | None = await self.photo_repo.delete(user.telegram_id)
        if deleted_photos is None:
            raise PhotosNotFound
        
        await self.file_storage.delete(deleted_photos)
        return