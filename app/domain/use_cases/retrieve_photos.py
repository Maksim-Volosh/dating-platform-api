from typing import List

from app.domain.entities import PhotoUrlEntity
from app.domain.entities.user import UserEntity
from app.domain.exceptions import PhotosNotFound, UserNotFoundById
from app.domain.interfaces import IPhotoRepository, IUserRepository


class RetrieveUserPhotosUseCase:
    def __init__(
        self,
        user_repo: IUserRepository, 
        photo_repo: IPhotoRepository, 
    ) -> None:
        self.photo_repo = photo_repo
        self.user_repo = user_repo
        
    async def execute(self, telegram_id: int) -> list[PhotoUrlEntity]:
        user: UserEntity | None = await self.user_repo.get_by_id(telegram_id)
        if user is None:
            raise UserNotFoundById
        
        photos: List[PhotoUrlEntity] | None = await self.photo_repo.get_by_user_id(telegram_id)
        if photos is None:
            raise PhotosNotFound
        return photos
