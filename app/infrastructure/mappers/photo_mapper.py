from typing import List

from app.api.v1.schemas.photo import PhotoFileId
from app.domain.entities import PhotoEntity


async def to_entities(photos: List[PhotoFileId]) -> List[PhotoEntity]:
    return [
        PhotoEntity(
            file_id=photo.file_id
        )
        for photo in photos
    ]
