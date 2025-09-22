from unittest.mock import AsyncMock

import pytest

from app.domain.entities import UserEntity
from app.domain.exceptions import UserNotFoundById
from app.domain.exceptions.deck import NoCandidatesFound
from app.domain.services.deck import DeckBuilderService
from app.domain.use_cases.deck import UserDeckUseCase


@pytest.fixture
def fake_user():
    return UserEntity(
        telegram_id=1,
        name="name",  
        age=18,
        city="city",
        gender="male",
        prefer_gender="female",
        description="description"
    )

# -------------------------------
# Tests for DeckBuilderService
# -------------------------------

@pytest.mark.asyncio
async def test_deck_builder_service_build_success(fake_user):
    candidate_repo = AsyncMock()
    candidate_repo.get_candidates_by_preferences.return_value = [fake_user, fake_user, fake_user, fake_user, fake_user]
    swipe_repo = AsyncMock()
    swipe_repo.was_swiped.side_effect = [False, False, False, True, True] 
    cache = AsyncMock()
    cache.delete.return_value = None
    cache.rpush.return_value = None
    
    use_case = DeckBuilderService(candidate_repo, swipe_repo, cache)

    candidates = await use_case.build(fake_user)

    assert candidates == [fake_user, fake_user, fake_user, fake_user, fake_user]
    candidate_repo.get_candidates_by_preferences.assert_awaited_once_with(fake_user.telegram_id, fake_user.city, fake_user.age, fake_user.gender, fake_user.prefer_gender)
    swipe_repo.was_swiped.assert_any_await(fake_user.telegram_id, fake_user.telegram_id)
    assert swipe_repo.was_swiped.await_count == 5
    cache.delete.assert_awaited_once_with(f"deck:{fake_user.telegram_id}")
    not_swiped_candidates = cache.rpush.await_args[0][1] 
    assert not_swiped_candidates == [fake_user, fake_user, fake_user]
    
@pytest.mark.asyncio
async def test_deck_builder_service_build_all_was_swiped(fake_user):
    candidate_repo = AsyncMock()
    candidate_repo.get_candidates_by_preferences.return_value = [fake_user, fake_user, fake_user, fake_user, fake_user]
    swipe_repo = AsyncMock()
    swipe_repo.was_swiped.side_effect = [True, True, True, True, True] 
    cache = AsyncMock()
    
    use_case = DeckBuilderService(candidate_repo, swipe_repo, cache)

    await use_case.build(fake_user)

    candidate_repo.get_candidates_by_preferences.assert_awaited_once_with(fake_user.telegram_id, fake_user.city, fake_user.age, fake_user.gender, fake_user.prefer_gender)
    swipe_repo.was_swiped.assert_any_await(fake_user.telegram_id, fake_user.telegram_id)
    assert swipe_repo.was_swiped.await_count == 5
    cache.delete.assert_not_awaited()
    cache.rpush.assert_not_awaited()
    
    
@pytest.mark.asyncio
async def test_delete_user_from_others_decks(fake_user):
    cache = AsyncMock()
    other_user = UserEntity(
        telegram_id=2,
        name="other",
        age=20,
        city="city",
        gender="female",
        prefer_gender="male",
        description="desc"
    )
    cache.get_deck.return_value = [fake_user, other_user]
    cache.delete.return_value = None
    cache.rpush.return_value = None

    candidate_repo = AsyncMock()
    swipe_repo = AsyncMock()
    service = DeckBuilderService(candidate_repo, swipe_repo, cache)

    await service._delete_user_from_others_decks(fake_user.telegram_id, [other_user])

    cache.get_deck.assert_awaited_once_with("deck:2")
    cache.delete.assert_awaited_once_with("deck:2")
    cache.rpush.assert_awaited_once()
    updated_deck = cache.rpush.await_args[0][1]
    assert updated_deck == [other_user]

@pytest.mark.asyncio
async def test_build_and_clean_others_with_candidates(fake_user):
    candidate_repo = AsyncMock()
    swipe_repo = AsyncMock()
    cache = AsyncMock()
    service = DeckBuilderService(candidate_repo, swipe_repo, cache)

    service.build = AsyncMock(return_value=[fake_user])  # подменяем build
    service._delete_user_from_others_decks = AsyncMock()

    await service.build_and_clean_others(fake_user)

    service.build.assert_awaited_once_with(fake_user)
    service._delete_user_from_others_decks.assert_awaited_once_with(fake_user.telegram_id, [fake_user])


@pytest.mark.asyncio
async def test_build_and_clean_others_no_candidates(fake_user):
    candidate_repo = AsyncMock()
    swipe_repo = AsyncMock()
    cache = AsyncMock()
    service = DeckBuilderService(candidate_repo, swipe_repo, cache)

    service.build = AsyncMock(return_value=None)
    service._delete_user_from_others_decks = AsyncMock()

    await service.build_and_clean_others(fake_user)

    service.build.assert_awaited_once_with(fake_user)
    service._delete_user_from_others_decks.assert_not_awaited()
