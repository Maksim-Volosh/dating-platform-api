from unittest.mock import AsyncMock

import pytest

from app.domain.entities import UserEntity, Gender, PreferGender, UserDistanceEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.deck import NoCandidatesFound
from app.application.use_cases.deck import UserDeckUseCase


@pytest.fixture
def fake_user():
    return UserEntity(
        telegram_id=1,
        name="name",
        age=18,
        latitude=0,
        longitude=0,
        gender=Gender("male"),
        prefer_gender=PreferGender("female"),
        description="description",
    )
    
@pytest.fixture
def fake_distance_user():
    return UserDistanceEntity(
        telegram_id=1,
        name="name",
        age=18,
        distance=1.123,
        gender=Gender("male"),
        prefer_gender=PreferGender("female"),
        description="description",
    )


# -------------------------------
# Tests for UserDeckUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_user_deck_use_case_get_from_cache(fake_user, fake_distance_user):
    cache = AsyncMock()
    cache.lpop.return_value = fake_distance_user
    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    geo_filter = AsyncMock()
    swipe_filter = AsyncMock()

    use_case = UserDeckUseCase(cache, deck_builder, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.next(fake_user)

    assert user != fake_user
    assert user == fake_distance_user
    cache.lpop.assert_awaited_once_with("deck:1")


@pytest.mark.asyncio
async def test_user_deck_use_case_build_deck(fake_user, fake_distance_user):
    cache = AsyncMock()
    cache.lpop.side_effect = [None, fake_distance_user]
    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    candidate_repo.find_by_preferences_and_bbox.return_value = [fake_user, fake_user]
    swipe_filter = AsyncMock()
    swipe_filter.filter.return_value = [fake_user, fake_user]
    geo_filter = AsyncMock()
    geo_filter.filter.return_value = [fake_distance_user, fake_distance_user]

    use_case = UserDeckUseCase(cache, deck_builder, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.next(fake_user)

    assert user == fake_distance_user
    assert candidate_repo.find_by_preferences_and_bbox.await_count == 1
    assert swipe_filter.filter.await_count == 1
    assert geo_filter.filter.await_count == 1
    assert cache.lpop.await_count == 2
    cache.lpop.assert_any_await("deck:1")
    deck_builder.build.assert_awaited_once_with(fake_user, [fake_distance_user, fake_distance_user])


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
