from typing import List

from app.domain.entities import (PhotoEntity, PhotoUniqueNameEntity,
                                 PhotoUrlEntity, UserEntity)
from app.domain.exceptions import (TooManyPhotos, UserNotFoundById,
                                   WrongFileExtension)
from app.domain.interfaces import (IPhotoRepository, IPhotoStorage,
                                   IUserRepository)


class UploadUserPhotosUseCase:
    def __init__(
        self,
        user_repo: IUserRepository, 
        photo_repo: IPhotoRepository, 
        file_storage: IPhotoStorage
    ) -> None:
        self.photo_repo = photo_repo
        self.user_repo = user_repo
        self.file_storage = file_storage
    
    async def execute(
        self, telegram_id: int, photos: List[PhotoEntity]
    ) -> List[PhotoUrlEntity]:
        user: UserEntity | None = await self.user_repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        
        user_photos = await self.photo_repo.get_by_user_id(telegram_id)
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
            
        urls: List[PhotoUrlEntity] = await self.photo_repo.create(telegram_id, unique_names) 
        return urls