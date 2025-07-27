from typing import List

from app.domain.entities import PhotoUrlEntity, UserEntity
from app.domain.exceptions import PhotosNotFound, UserNotFoundById
from app.domain.interfaces import (IPhotoRepository, IPhotoStorage,
                                   IUserRepository)


class DeleteUserPhotosUseCase:
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
        self, telegram_id: int
    ) -> None:
        user: UserEntity | None = await self.user_repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        
        deleted_photos: List[PhotoUrlEntity] | None = await self.photo_repo.delete(telegram_id)
        if deleted_photos is None:
            raise PhotosNotFound
        
        await self.file_storage.delete(deleted_photos)
        return
        
        