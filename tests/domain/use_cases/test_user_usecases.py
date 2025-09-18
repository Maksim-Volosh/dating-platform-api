from unittest.mock import AsyncMock, patch

import pytest

from app.domain.entities import UserEntity
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)
from app.domain.use_cases.user import (CreateUserUseCase, UpdateUserUseCase,
                                       UserUseCase)


@pytest.fixture
def fake_user():
    return UserEntity(
        telegram_id=1,
        name="Maxim",
        age=18,
        city="Vilnius",
        gender="male",
        prefer_gender="female",
        description="Test user"
    )


# -------------------------------
# Tests for UserUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_get_by_id_success(fake_user):
    repo = AsyncMock()
    repo.get_by_id.return_value = fake_user
    
    use_case = UserUseCase(repo)

    user = await use_case.get_by_id(1)

    assert user == fake_user
    repo.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None
    
    use_case = UserUseCase(repo)

    with pytest.raises(UserNotFoundById):
        await use_case.get_by_id(99)


@pytest.mark.asyncio
async def test_get_all_success(fake_user):
    repo = AsyncMock()
    repo.get_all.return_value = [fake_user]
    
    use_case = UserUseCase(repo)

    users = await use_case.get_all()

    assert len(users) == 1
    assert users[0].telegram_id == 1
    repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_empty():
    repo = AsyncMock()
    repo.get_all.return_value = None
    
    use_case = UserUseCase(repo)

    with pytest.raises(UsersNotFound):
        await use_case.get_all()


# -------------------------------
# Tests for CreateUserUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_create_user_success(fake_user):
    repo = AsyncMock()
    repo.create.return_value = fake_user
    deck_builder = AsyncMock()
    deck_builder.build_and_clean_others = AsyncMock(return_value=None)
    
    use_case = CreateUserUseCase(repo, deck_builder)

    with patch("asyncio.create_task") as mock_task:
        user = await use_case.execute(fake_user)

    assert user == fake_user
    repo.create.assert_awaited_once_with(fake_user)
    mock_task.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_already_exists(fake_user):
    repo = AsyncMock()
    repo.create.return_value = None
    deck_builder = AsyncMock()
    
    use_case = CreateUserUseCase(repo, deck_builder)

    with pytest.raises(UserAlreadyExists):
        await use_case.execute(fake_user)


# -------------------------------
# Tests for UpdateUserUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_update_user_success(fake_user):
    repo = AsyncMock()
    repo.update.return_value = fake_user
    deck_builder = AsyncMock()
    deck_builder.build_and_clean_others = AsyncMock(return_value=None)
    cache = AsyncMock()
    
    use_case = UpdateUserUseCase(repo, deck_builder, cache)

    with patch("asyncio.create_task") as mock_task:
        user = await use_case.execute(fake_user.telegram_id, fake_user)

    assert user == fake_user
    repo.update.assert_awaited_once_with(fake_user.telegram_id, fake_user)
    mock_task.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_not_found(fake_user):
    repo = AsyncMock()
    repo.update.return_value = None
    deck_builder = AsyncMock()
    cache = AsyncMock()
    
    use_case = UpdateUserUseCase(repo, deck_builder, cache)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(fake_user.telegram_id, fake_user)
