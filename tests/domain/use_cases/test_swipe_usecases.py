from unittest.mock import AsyncMock

import pytest

from app.application.use_cases import SwipeUserUseCase
from app.domain.entities import SwipeEntity

# -------------------------------
# Tests for SwipeUserUseCase
# -------------------------------


@pytest.mark.asyncio
async def test_swipe_user_use_case_success_not_exists_1():
    swipe_repo = AsyncMock()
    swipe_repo.get_by_ids.return_value = None
    inbox_service = AsyncMock()

    use_case = SwipeUserUseCase(swipe_repo, inbox_service)
    swipe = SwipeEntity(liker_id=10, liked_id=5, decision=True)

    result = await use_case.execute(swipe)

    swipe_repo.create.assert_awaited_once()
    normalized_swipe = swipe_repo.create.await_args[0][0]

    assert normalized_swipe.user1_id == 5
    assert normalized_swipe.user2_id == 10
    assert normalized_swipe.decision is True
    assert normalized_swipe.liker_is_user1 is False


@pytest.mark.asyncio
async def test_swipe_user_use_case_success_not_exists_2():
    swipe_repo = AsyncMock()
    swipe_repo.get_by_ids.return_value = None
    inbox_service = AsyncMock()

    use_case = SwipeUserUseCase(swipe_repo, inbox_service)
    swipe = SwipeEntity(liker_id=5, liked_id=10, decision=True)

    result = await use_case.execute(swipe)

    swipe_repo.create.assert_awaited_once()
    normalized_swipe = swipe_repo.create.await_args[0][0]

    assert normalized_swipe.user1_id == 5
    assert normalized_swipe.user2_id == 10
    assert normalized_swipe.decision is True
    assert normalized_swipe.liker_is_user1 is True


@pytest.mark.asyncio
async def test_swipe_user_use_case_success_exists_1():
    swipe_repo = AsyncMock()
    swipe_repo.get_by_ids.return_value = "Not none"
    inbox_service = AsyncMock()

    use_case = SwipeUserUseCase(swipe_repo, inbox_service)
    swipe = SwipeEntity(liker_id=10, liked_id=5, decision=True)

    result = await use_case.execute(swipe)

    swipe_repo.update.assert_awaited_once()
    normalized_swipe = swipe_repo.update.await_args[0][1]

    assert normalized_swipe.user1_id == 5
    assert normalized_swipe.user2_id == 10
    assert normalized_swipe.decision is True
    assert normalized_swipe.liker_is_user1 is False


@pytest.mark.asyncio
async def test_swipe_user_use_case_success_exists_2():
    swipe_repo = AsyncMock()
    swipe_repo.get_by_ids.return_value = "Not none"
    inbox_service = AsyncMock()

    use_case = SwipeUserUseCase(swipe_repo, inbox_service)
    swipe = SwipeEntity(liker_id=5, liked_id=10, decision=True)

    result = await use_case.execute(swipe)

    swipe_repo.update.assert_awaited_once()
    normalized_swipe = swipe_repo.update.await_args[0][1]

    assert normalized_swipe.user1_id == 5
    assert normalized_swipe.user2_id == 10
    assert normalized_swipe.decision is True
    assert normalized_swipe.liker_is_user1 is True
