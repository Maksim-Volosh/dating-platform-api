from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.entities import PhotoUniqueNameEntity, PhotoUrlEntity
from app.domain.interfaces import IPhotoRepository
from app.infrastructure.models import Photo


class SQLAlchemyPhotoRepository(IPhotoRepository):
    def __init__(self, session) -> None:
        self.session: AsyncSession = session
        
    async def get_by_user_id(self, telegram_id: int) -> List[PhotoUrlEntity] | None:
        q = select(Photo).where(Photo.user_id == telegram_id)
        result = await self.session.execute(q)
        photo_models = result.scalars().all()
        
        if not photo_models:
            return None

        return [PhotoUrlEntity(url=photo.url) for photo in photo_models]
    
    async def create(
        self, telegram_id: int, unique_names: List[PhotoUniqueNameEntity]
    ) -> List[PhotoUrlEntity]:
        photo_objs = []
        for unique_name in unique_names:
            new_photo = Photo(
                url=f"{settings.static.url}/{unique_name.name}", user_id=telegram_id
                )
            photo_objs.append(new_photo)
            
        for photo in photo_objs:
            self.session.add(photo)
        await self.session.commit()
        return [PhotoUrlEntity(url=photo.url) for photo in photo_objs]
    
    async def delete(self, telegram_id: int) -> List[PhotoUrlEntity] | None:
        q = select(Photo).where(Photo.user_id == telegram_id)
        result = await self.session.execute(q)
        photos_models = result.scalars().all()
        
        if photos_models is None:
            return None
        
        photo_urls = []
        for photo in photos_models:
            photo_urls.append(PhotoUrlEntity(url=photo.url))
            await self.session.delete(photo)
            
        await self.session.commit()
        return photo_urls