import os
import uuid
from typing import List

import aiofiles

from app.core.config import settings
from app.domain.entities import (PhotoEntity, PhotoUniqueNameEntity,
                                 PhotoUrlEntity)
from app.domain.interfaces import IPhotoStorage


class LocalPhotoStorage(IPhotoStorage):
    async def save(self, files: List[PhotoEntity]) -> List[PhotoUniqueNameEntity] | None:
        unique_names = []
        for file in files:
            if not file.content_type.startswith("image"):
                return None
            
            contents = file.content
            unique_name = f"{uuid.uuid4()}_{file.filename}"
            save_path = os.path.join(settings.static.directory, unique_name)

            async with aiofiles.open(save_path, "wb") as f:
                await f.write(contents)
            
            unique_names.append(PhotoUniqueNameEntity(name=unique_name))
        return unique_names
    
    async def delete(self, photo_urls: List[PhotoUrlEntity]) -> None:
        for photo_url in photo_urls:
            try:
                os.remove("." + photo_url.url)
            except FileNotFoundError:
                continue
        return 
    
    