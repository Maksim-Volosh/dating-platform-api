from unittest.mock import AsyncMock, Mock

import pytest

from app.application.use_cases.deck import UserDeckUseCase
from app.core.config import settings
from app.domain.entities import Gender, PreferGender, UserDistanceEntity, UserEntity
from app.domain.exceptions import NoCandidatesFound, UserNotFoundById


@pytest.fixture
def fake_user() -> UserEntity:
    return UserEntity(
        telegram_id=1,
        name="name",
        age=18,
        latitude=10.0,
        longitude=20.0,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="description",
    )


@pytest.fixture
def fake_distance_user() -> UserDistanceEntity:
    return UserDistanceEntity(
        telegram_id=2,
        name="cand",
        age=19,
        distance=1.123,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="candidate desc",
    )


@pytest.mark.asyncio
async def test_user_deck_next_gets_from_cache(fake_user, fake_distance_user):
    cache = AsyncMock()
    cache.lpop.return_value = fake_distance_user

    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    geo_filter = AsyncMock()
    swipe_filter = AsyncMock()

    use_case = UserDeckUseCase(
        cache, deck_builder, candidate_repo, geo_filter, swipe_filter
    )

    result = await use_case.next(fake_user)

    assert result == fake_distance_user
    cache.lpop.assert_awaited_once_with("deck:1")

    candidate_repo.find_by_preferences_and_bbox.assert_not_awaited()
    swipe_filter.filter.assert_not_awaited()
    geo_filter.filter.assert_not_awaited()
    deck_builder.build.assert_not_awaited()


@pytest.mark.asyncio
async def test_user_deck_next_builds_deck_when_cache_empty(
    fake_user, fake_distance_user, monkeypatch
):
    cache = AsyncMock()
    cache.lpop.side_effect = [None, fake_distance_user]

    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    swipe_filter = AsyncMock()
    geo_filter = AsyncMock()

    bbx_sentinel = object()
    bounding_box_mock = Mock(return_value=bbx_sentinel)
    monkeypatch.setattr(
        "app.application.use_cases.deck.bounding_box", bounding_box_mock
    )

    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    candidates = [AsyncMock(spec=UserEntity), AsyncMock(spec=UserEntity)]
    candidate_repo.find_by_preferences_and_bbox.return_value = candidates

    swipe_filtered = [AsyncMock(spec=UserEntity)]
    swipe_filter.filter.return_value = swipe_filtered

    geo_filtered = [fake_distance_user]
    geo_filter.filter.return_value = geo_filtered

    use_case = UserDeckUseCase(
        cache, deck_builder, candidate_repo, geo_filter, swipe_filter
    )

    result = await use_case.next(fake_user)

    assert result == fake_distance_user

    assert cache.lpop.await_count == 2
    cache.lpop.assert_any_await("deck:1")

    bounding_box_mock.assert_called_once_with(
        fake_user.latitude, fake_user.longitude, 30
    )

    candidate_repo.find_by_preferences_and_bbox.assert_awaited_once_with(
        fake_user, bbx_sentinel
    )
    swipe_filter.filter.assert_awaited_once_with(fake_user.telegram_id, candidates)
    geo_filter.filter.assert_awaited_once_with(fake_user, swipe_filtered)

    deck_builder.build.assert_awaited_once_with(fake_user, geo_filtered)


@pytest.mark.asyncio
async def test_user_deck_next_raises_no_candidates_found(fake_user, monkeypatch):
    cache = AsyncMock()
    cache.lpop.return_value = None

    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    swipe_filter = AsyncMock()
    geo_filter = AsyncMock()

    bbx_sentinel = object()
    monkeypatch.setattr(
        "app.application.use_cases.deck.bounding_box", Mock(return_value=bbx_sentinel)
    )
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    candidate_repo.find_by_preferences_and_bbox.return_value = [
        AsyncMock(spec=UserEntity)
    ]
    swipe_filter.filter.return_value = [AsyncMock(spec=UserEntity)]
    geo_filter.filter.return_value = []  # <- ключевой момент

    use_case = UserDeckUseCase(
        cache, deck_builder, candidate_repo, geo_filter, swipe_filter
    )

    with pytest.raises(NoCandidatesFound):
        await use_case.next(fake_user)

    deck_builder.build.assert_not_awaited()
    cache.lpop.assert_awaited_once_with("deck:1")


@pytest.mark.asyncio
async def test_user_deck_next_raises_user_not_found_by_id_when_still_empty_after_build(
    fake_user, monkeypatch
):
    cache = AsyncMock()
    cache.lpop.side_effect = [None, None]

    deck_builder = AsyncMock()
    candidate_repo = AsyncMock()
    swipe_filter = AsyncMock()
    geo_filter = AsyncMock()

    bbx_sentinel = object()
    monkeypatch.setattr(
        "app.application.use_cases.deck.bounding_box", Mock(return_value=bbx_sentinel)
    )
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    candidate_repo.find_by_preferences_and_bbox.return_value = [
        AsyncMock(spec=UserEntity)
    ]
    swipe_filter.filter.return_value = [AsyncMock(spec=UserEntity)]
    geo_filter.filter.return_value = [
        AsyncMock(spec=UserDistanceEntity)
    ]  # не пусто, build должен быть

    use_case = UserDeckUseCase(
        cache, deck_builder, candidate_repo, geo_filter, swipe_filter
    )

    with pytest.raises(UserNotFoundById):
        await use_case.next(fake_user)

    assert cache.lpop.await_count == 2
    deck_builder.build.assert_awaited_once()
