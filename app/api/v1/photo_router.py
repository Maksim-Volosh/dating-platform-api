import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.photo_schemas import PhotoCreateResponse, PhotoURL
from app.config import settings
from app.infrastructure.db import db_helper
from app.infrastructure.models.users import Photo, User

router = APIRouter()


@router.post("/{user_id}/photos")
async def upload_user_photos(
    user_id: int,
    photos: List[UploadFile],
    db: AsyncSession = Depends(db_helper.session_getter)
) -> PhotoCreateResponse:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with Id: {user_id} not found")

    photo_objs = []
    for file in photos:
        
        file_ext = os.path.splitext(f"{file.filename}")[1].lower()
        if file_ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(400, f"You can upload only .jpg, .jpeg, .png or .webp files but not {file_ext}")
        
        contents = await file.read()
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        save_path = os.path.join(settings.static.directory, unique_name)

        with open(save_path, "wb") as f:
            f.write(contents)

        new_photo = Photo(url=f"/{settings.static.url}/{unique_name}", user_id=user_id)
        db.add(new_photo)
        photo_objs.append(new_photo)

    await db.commit()

    return PhotoCreateResponse(
        user_id=user_id,
        photos=[PhotoURL(url=p.url) for p in photo_objs]
    )


