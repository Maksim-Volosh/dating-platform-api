from typing import List

from fastapi import UploadFile

from app.domain.entities import PhotoEntity


async def to_entities(photos: List[UploadFile]) -> List[PhotoEntity]:
    return [
        PhotoEntity(
            filename=photo.filename,
            content=await photo.read(),
            content_type=photo.content_type,
        )
        for photo in photos
        if photo.filename and photo.content_type
    ]
