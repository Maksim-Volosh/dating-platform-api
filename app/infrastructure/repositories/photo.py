from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import PhotoEntity
from app.domain.interfaces import IPhotoRepository
from app.infrastructure.models import Photo


class SQLAlchemyPhotoRepository(IPhotoRepository):
    def __init__(self, session) -> None:
        self.session: AsyncSession = session
        
    async def get_by_user_id(self, telegram_id: int) -> List[PhotoEntity] | None:
        q = select(Photo).where(Photo.user_id == telegram_id)
        result = await self.session.execute(q)
        photo_models = result.scalars().all()
        
        if not photo_models:
            return None

        return [PhotoEntity(file_id=photo.file_id) for photo in photo_models]
    
    async def create(
        self, telegram_id: int, photos: List[PhotoEntity]
    ) -> List[PhotoEntity]:
        photo_objs = []
        for photo in photos:
            new_photo = Photo(
                file_id=photo.file_id, user_id=telegram_id
                )
            photo_objs.append(new_photo)
            
        for photo in photo_objs:
            self.session.add(photo)
        await self.session.commit()
        return [PhotoEntity(file_id=photo.file_id) for photo in photo_objs]
    
    async def delete(self, telegram_id: int) -> List[PhotoEntity] | None:
        q = select(Photo).where(Photo.user_id == telegram_id)
        result = await self.session.execute(q)
        photos_models = result.scalars().all()
        
        if photos_models is None:
            return None
        
        photo_file_ids = []
        for photo in photos_models:
            photo_file_ids.append(PhotoEntity(file_id=photo.file_id))
            await self.session.delete(photo)
            
        await self.session.commit()
        return photo_file_ids