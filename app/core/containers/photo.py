from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases import (DeleteUserPhotosUseCase,
                                  RetrieveUserPhotosUseCase,
                                  UpdateUserPhotosUseCase,
                                  UploadUserPhotosUseCase)
from app.infrastructure.db import db_helper
from app.infrastructure.repositories import (LocalPhotoStorage,
                                             SQLAlchemyPhotoRepository)


async def get_retrieve_user_photos_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> RetrieveUserPhotosUseCase:
    photo_repo = SQLAlchemyPhotoRepository(db)
    return RetrieveUserPhotosUseCase(
        photo_repo=photo_repo,
    )
    
async def get_upload_user_photos_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UploadUserPhotosUseCase:
    photo_repo = SQLAlchemyPhotoRepository(db)
    return UploadUserPhotosUseCase(
        photo_repo=photo_repo,
        file_storage=file_storage
    )
    
async def get_delete_user_photos_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> DeleteUserPhotosUseCase:
    photo_repo = SQLAlchemyPhotoRepository(db)
    file_storage = LocalPhotoStorage()
    return DeleteUserPhotosUseCase(
        photo_repo=photo_repo,
        file_storage=file_storage
    )
    
async def get_update_user_photos_use_case(
    db: AsyncSession = Depends(db_helper.session_getter)
) -> UpdateUserPhotosUseCase:
    photo_repo = SQLAlchemyPhotoRepository(db)
    file_storage = LocalPhotoStorage()
    return UpdateUserPhotosUseCase(
        photo_repo=photo_repo,
        file_storage=file_storage
    )

