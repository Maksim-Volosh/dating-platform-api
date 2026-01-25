from unittest.mock import AsyncMock

import pytest

from app.domain.entities import UserEntity, Gender, PreferGender
from app.domain.entities.photo import PhotoEntity
from app.domain.exceptions.photo import (
    PhotosNotFound,
    TooManyPhotos,
    WrongFileExtension,
)
from app.application.use_cases import RetrieveUserPhotosUseCase
from app.application.use_cases.photo import (
    DeleteUserPhotosUseCase,
    UpdateUserPhotosUseCase,
    UploadUserPhotosUseCase,
)


@pytest.fixture
def fake_user():
    return UserEntity(
        telegram_id=1,
        name="Maxim",
        age=18,
        city="Vilnius",
        gender=Gender("male"),
        prefer_gender=PreferGender("female"),
        description="Test user",
    )


@pytest.fixture
def fake_photo_entity():
    return PhotoEntity(file_id="test_file_id")


# -------------------------------
# Tests for RetrieveUserPhotosUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_get_by_user_id_success(fake_user, fake_photo_entity):
    photo_repo = AsyncMock()
    photo_repo.get_by_user_id.return_value = [fake_photo_entity]

    use_case = RetrieveUserPhotosUseCase(photo_repo)

    user = await use_case.execute(fake_user)

    assert user == [fake_photo_entity]
    photo_repo.get_by_user_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_by_user_id_not_found(fake_user):
    photo_repo = AsyncMock()
    photo_repo.get_by_user_id.return_value = None

    use_case = RetrieveUserPhotosUseCase(photo_repo)

    with pytest.raises(PhotosNotFound):
        await use_case.execute(fake_user)


# -------------------------------
# Tests for UploadUserPhotosUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_upload_user_photo_success(fake_user, fake_photo_entity):

    photo_repo = AsyncMock()
    photo_repo.get_by_user_id.return_value = None
    photo_repo.create.return_value = [fake_photo_entity, fake_photo_entity]

    use_case = UploadUserPhotosUseCase(photo_repo)
    photos = await use_case.execute(fake_user, [fake_photo_entity, fake_photo_entity])

    assert photos == [fake_photo_entity, fake_photo_entity]
    photo_repo.get_by_user_id.assert_awaited_once_with(1)
    photo_repo.create.assert_awaited_once_with(
        1, [fake_photo_entity, fake_photo_entity]
    )


@pytest.mark.asyncio
async def test_upload_user_photo_too_many_photos_exists(
    fake_user,
    fake_photo_entity,
):

    photo_repo = AsyncMock()
    photo_repo.get_by_user_id.return_value = [
        fake_photo_entity,
        fake_photo_entity,
        fake_photo_entity,
    ]

    file_storage = AsyncMock()

    use_case = UploadUserPhotosUseCase(photo_repo)
    with pytest.raises(TooManyPhotos):
        await use_case.execute(fake_user, [fake_photo_entity, fake_photo_entity])


@pytest.mark.asyncio
async def test_upload_user_photo_too_many_photos_uploaded(fake_user, fake_photo_entity):

    photo_repo = AsyncMock()
    photo_repo.get_by_user_id.return_value = [fake_photo_entity, fake_photo_entity]

    use_case = UploadUserPhotosUseCase(photo_repo)
    with pytest.raises(TooManyPhotos):
        await use_case.execute(fake_user, [fake_photo_entity, fake_photo_entity])


# -------------------------------
# Tests for UpdateUserPhotosUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_update_user_photo_success(fake_user, fake_photo_entity):

    photo_repo = AsyncMock()
    photo_repo.delete.return_value = [fake_photo_entity, fake_photo_entity]
    photo_repo.create.return_value = [fake_photo_entity, fake_photo_entity]

    use_case = UpdateUserPhotosUseCase(photo_repo)
    photos = await use_case.execute(fake_user, [fake_photo_entity, fake_photo_entity])

    assert photos == [fake_photo_entity, fake_photo_entity]
    photo_repo.delete.assert_awaited_once_with(1)
    photo_repo.create.assert_awaited_once_with(
        1, [fake_photo_entity, fake_photo_entity]
    )


@pytest.mark.asyncio
async def test_update_user_photo_with_too_many_photos(fake_user, fake_photo_entity):

    photo_repo = AsyncMock()
    photo_repo.delete.return_value = None
    photo_repo.create.return_value = [fake_photo_entity, fake_photo_entity]

    use_case = UpdateUserPhotosUseCase(photo_repo)
    with pytest.raises(TooManyPhotos):
        await use_case.execute(
            fake_user,
            [
                fake_photo_entity,
                fake_photo_entity,
                fake_photo_entity,
                fake_photo_entity,
            ],
        )


# -------------------------------
# Tests for DeleteUserPhotosUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_delete_user_photo_success(fake_user, fake_photo_entity):

    photo_repo = AsyncMock()
    photo_repo.delete.return_value = [fake_photo_entity, fake_photo_entity]

    use_case = DeleteUserPhotosUseCase(photo_repo)
    await use_case.execute(fake_user)

    photo_repo.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_user_photo_photos_not_found(
    fake_user,
):

    photo_repo = AsyncMock()
    photo_repo.delete.return_value = None

    use_case = DeleteUserPhotosUseCase(photo_repo)
    with pytest.raises(PhotosNotFound):
        await use_case.execute(fake_user)
