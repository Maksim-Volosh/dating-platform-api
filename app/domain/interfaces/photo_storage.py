from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import PhotoEntity, PhotoUniqueNameEntity, PhotoUrlEntity


class IPhotoStorage(ABC):
    @abstractmethod
    async def save(self, files: List[PhotoEntity]) -> List[PhotoUniqueNameEntity] | None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, photo_urls: List[PhotoUrlEntity]) -> None:
        raise NotImplementedError
    
    