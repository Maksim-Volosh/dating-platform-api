from unittest.mock import AsyncMock

import pytest

from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.deck import NoCandidatesFound
from app.domain.use_cases.deck import UserDeckUseCase


@pytest.fixture
def fake_user():
    return UserEntity(
        telegram_id=1,
        name="name",  
        age=18,
        city="city",
        gender="gender",
        prefer_gender="prefer_gender",
        description="description"
    )

# -------------------------------
# Tests for UserDeckUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_user_deck_use_case_get_from_cache(fake_user):
    cache = AsyncMock()
    cache.lpop.return_value = fake_user 
    deck_builder = AsyncMock()
    
    use_case = UserDeckUseCase(cache, deck_builder)

    user = await use_case.next(fake_user)

    assert user == fake_user
    cache.lpop.assert_awaited_once_with("deck:1")
    
@pytest.mark.asyncio
async def test_user_deck_use_case_build_deck(fake_user):
    cache = AsyncMock()
    cache.lpop.side_effect = [None, fake_user] 
    deck_builder = AsyncMock()
    deck_builder.build.return_value = [fake_user]
    
    use_case = UserDeckUseCase(cache, deck_builder)

    user = await use_case.next(fake_user)

    assert user == fake_user
    assert cache.lpop.await_count == 2
    cache.lpop.assert_any_await("deck:1")
    deck_builder.build.assert_awaited_once_with(fake_user)
    
@pytest.mark.asyncio
async def test_user_deck_use_case_no_candidates(fake_user):
    cache = AsyncMock()
    cache.lpop.return_value = None
    deck_builder = AsyncMock()
    deck_builder.build.return_value = None
    
    use_case = UserDeckUseCase(cache, deck_builder)

    with pytest.raises(NoCandidatesFound): 
        await use_case.next(fake_user)
    
@pytest.mark.asyncio
async def test_user_deck_use_case_user_not_found(fake_user):
    cache = AsyncMock()
    cache.lpop.side_effect = [None, None]
    deck_builder = AsyncMock()
    deck_builder.build.return_value = [fake_user, fake_user]
    
    use_case = UserDeckUseCase(cache, deck_builder)

    with pytest.raises(UserNotFoundById): 
        await use_case.next(fake_user)