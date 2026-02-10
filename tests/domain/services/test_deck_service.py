from unittest.mock import AsyncMock

import pytest

from app.application.services.deck import DeckBuilderService
from app.domain.entities import Gender, PreferGender, UserDistanceEntity, UserEntity


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
        telegram_id=99,
        name="cand",
        age=22,
        distance=1.123,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="cand desc",
    )


# -------------------------------
# Tests for DeckBuilderService
# -------------------------------


@pytest.mark.asyncio
async def test_deck_builder_build_deletes_old_and_pushes_new(
    fake_user, fake_distance_user, monkeypatch
):
    # arrange
    cache = AsyncMock()
    cache.delete.return_value = None
    cache.rpush.return_value = None

    # чтобы тест не флапал из-за random.shuffle
    monkeypatch.setattr("app.application.services.deck.random.shuffle", lambda x: None)

    service = DeckBuilderService(cache=cache)
    candidates = [
        fake_distance_user,
        UserDistanceEntity(**{**fake_distance_user.to_dict(), "telegram_id": 100}),
        UserDistanceEntity(**{**fake_distance_user.to_dict(), "telegram_id": 101}),
    ]

    # act
    result = await service.build(fake_user, candidates)

    # assert
    assert result == candidates

    key = f"deck:{fake_user.telegram_id}"
    cache.delete.assert_awaited_once_with(key)

    # rpush(key, users, timeout=...)
    assert cache.rpush.await_count == 1
    args, kwargs = cache.rpush.await_args
    assert args[0] == key
    assert args[1] == candidates
    assert (
        "timeout" in kwargs
    )  # конкретное число можно тоже проверить, но это уже тест настроек


@pytest.mark.asyncio
async def test_deck_builder_build_trims_to_max_size(
    fake_user, fake_distance_user, monkeypatch
):
    """
    Check that candidates are trimmed to settings.deck.max_size.
    (Important: this works only if max_size in config is less than the length of the list.)
    """
    cache = AsyncMock()
    cache.delete.return_value = None
    cache.rpush.return_value = None

    monkeypatch.setattr("app.application.services.deck.random.shuffle", lambda x: None)

    service = DeckBuilderService(cache=cache)

    candidates = [
        UserDistanceEntity(**{**fake_distance_user.to_dict(), "telegram_id": i})
        for i in range(1, 151)
    ]

    result = await service.build(fake_user, candidates)

    assert len(result) <= 100

    args, _ = cache.rpush.await_args
    pushed_users = args[1]
    assert len(pushed_users) <= 100


@pytest.mark.asyncio
async def test_clean_others_removes_user_from_other_deck_when_present(fake_user):
    cache = AsyncMock()
    cache.delete.return_value = None
    cache.rpush.return_value = None

    suspicious = UserEntity(
        telegram_id=2,
        name="sus",
        age=20,
        latitude=1.0,
        longitude=2.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="sus",
    )

    other_item = UserDistanceEntity(
        telegram_id=777,
        name="other",
        age=30,
        distance=3.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description=None,
    )
    deck_item_for_user = UserDistanceEntity(
        telegram_id=fake_user.telegram_id,
        name="name",
        age=18,
        distance=0.5,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="description",
    )

    cache.get_deck.return_value = [deck_item_for_user, other_item]

    service = DeckBuilderService(cache=cache)

    await service.clean_others(fake_user, [suspicious])

    cache.get_deck.assert_awaited_once_with("deck:2")
    cache.delete.assert_awaited_once_with("deck:2")
    cache.rpush.assert_awaited_once()

    args, kwargs = cache.rpush.await_args
    assert args[0] == "deck:2"
    assert args[1] == [other_item]
    assert "timeout" in kwargs


@pytest.mark.asyncio
async def test_clean_others_does_nothing_if_deck_is_none(fake_user):
    cache = AsyncMock()
    cache.get_deck.return_value = None

    suspicious = UserEntity(
        telegram_id=2,
        name="sus",
        age=20,
        latitude=1.0,
        longitude=2.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="sus",
    )

    service = DeckBuilderService(cache=cache)

    await service.clean_others(fake_user, [suspicious])

    cache.get_deck.assert_awaited_once_with("deck:2")
    cache.delete.assert_not_awaited()
    cache.rpush.assert_not_awaited()


@pytest.mark.asyncio
async def test_clean_others_does_nothing_if_user_not_in_deck(fake_user):
    cache = AsyncMock()
    cache.delete.return_value = None
    cache.rpush.return_value = None

    suspicious = UserEntity(
        telegram_id=2,
        name="sus",
        age=20,
        latitude=1.0,
        longitude=2.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="sus",
    )

    cache.get_deck.return_value = [
        UserDistanceEntity(
            telegram_id=777,
            name="other",
            age=30,
            distance=3.0,
            gender=Gender.FEMALE,
            prefer_gender=PreferGender.MALE,
            description=None,
        )
    ]

    service = DeckBuilderService(cache=cache)

    await service.clean_others(fake_user, [suspicious])

    cache.get_deck.assert_awaited_once_with("deck:2")
    cache.delete.assert_not_awaited()
    cache.rpush.assert_not_awaited()
