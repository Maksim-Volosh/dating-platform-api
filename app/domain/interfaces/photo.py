from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.photo import PhotoEntity


class IPhotoRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, telegram_id: int) -> List[PhotoEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, telegram_id: int, photos: List[PhotoEntity]
    ) -> List[PhotoEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, telegram_id: int) -> List[PhotoEntity] | None:
        raise NotImplementedError