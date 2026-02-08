from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import BBoxEntity, UserEntity


class ICandidateRepository(ABC):
    @abstractmethod
    async def find_by_preferences_and_bbox(
        self, user: UserEntity, bbox: BBoxEntity
    ) -> List[UserEntity]:
        raise NotImplementedError
