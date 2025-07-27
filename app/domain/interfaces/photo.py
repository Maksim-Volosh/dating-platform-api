from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.photo import PhotoUniqueNameEntity, PhotoUrlEntity


class IPhotoRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, telegram_id: int) -> List[PhotoUrlEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, telegram_id: int, unique_names: List[PhotoUniqueNameEntity]
    ) -> List[PhotoUrlEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, telegram_id: int) -> List[PhotoUrlEntity] | None:
        raise NotImplementedError