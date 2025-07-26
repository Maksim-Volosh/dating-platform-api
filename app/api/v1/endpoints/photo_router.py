import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.photo_schemas import PhotoResponse, PhotoURL
from app.config import settings
from app.infrastructure.db import db_helper
from app.infrastructure.models.photos import Photo
from app.infrastructure.models.users import User
import aiofiles

router = APIRouter(prefix="/users", tags=["User Photos"])


@router.get("/{user_id}/photos", status_code=200)
async def get_user_photos(
    user_id: int,
    db: AsyncSession = Depends(db_helper.session_getter)
) -> PhotoResponse:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with Id: {user_id} not found"
        )
    
    q = select(Photo).where(Photo.user_id == user_id)
    result = await db.execute(q)
    photos_models = result.scalars().all()
    
    return PhotoResponse(
        user_id=user_id,
        photos=[PhotoURL.model_validate(photo, from_attributes=True) 
                for photo in photos_models]
    )
    
@router.delete("/{user_id}/photos", status_code=204)
async def delete_user_photos(
    user_id: int,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with Id: {user_id} not found"
        )
    
    q = select(Photo).where(Photo.user_id == user_id)
    result = await db.execute(q)
    photos_models = result.scalars().all()
    
    for photo in photos_models:
        await db.delete(photo)
        
    await db.commit()
    return
    
@router.post("/{user_id}/photos", status_code=201)
async def upload_user_photos(
    user_id: int,
    photos: List[UploadFile],
    db: AsyncSession = Depends(db_helper.session_getter)
) -> PhotoResponse:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with Id: {user_id} not found"
            )

    photo_objs = []
    for file in photos:
        
        file_ext = os.path.splitext(f"{file.filename}")[1].lower()
        if file_ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(
                400, 
                f"You can upload only .jpg, .jpeg, .png or .webp files but not {file_ext}"
                )
        
        contents = await file.read()
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        save_path = os.path.join(settings.static.directory, unique_name)

        async with aiofiles.open(save_path, "wb") as f:
            await f.write(contents)

        new_photo = Photo(
            url=f"{settings.static.url}/{unique_name}", user_id=user_id
            )
        db.add(new_photo)
        photo_objs.append(new_photo)

    await db.commit()

    return PhotoResponse(
        user_id=user_id,
        photos=[PhotoURL(url=p.url) for p in photo_objs]
    )
    
@router.put("/{user_id}/photos", status_code=201)
async def update_user_photos(
    user_id: int,
    photos: List[UploadFile],
    db: AsyncSession = Depends(db_helper.session_getter)
) -> PhotoResponse:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with Id: {user_id} not found"
            )
    
    q = select(Photo).where(Photo.user_id == user_id)
    result = await db.execute(q)
    photos_models = result.scalars().all()

    for photo in photos_models:
        await db.delete(photo)
        
    photo_objs = []
    for file in photos:
        
        file_ext = os.path.splitext(f"{file.filename}")[1].lower()
        if file_ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(
                400, 
                f"You can upload only .jpg, .jpeg, .png or .webp files but not {file_ext}"
            )
        
        contents = await file.read()
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        save_path = os.path.join(settings.static.directory, unique_name)

        async with aiofiles.open(save_path, "wb") as f:
            await f.write(contents)

        new_photo = Photo(url=f"{settings.static.url}/{unique_name}", user_id=user_id)
        db.add(new_photo)
        photo_objs.append(new_photo)

    await db.commit()

    return PhotoResponse(
        user_id=user_id,
        photos=[PhotoURL(url=p.url) for p in photo_objs]
    )