from unittest.mock import AsyncMock

import pytest

from app.application.services.swipe_filter import SwipeFilterService
from app.domain.entities import Gender, PreferGender, UserEntity


@pytest.fixture
def candidates() -> list[UserEntity]:
    return [
        UserEntity(
            telegram_id=1,
            name="u1",
            age=18,
            latitude=10.0,
            longitude=20.0,
            gender=Gender.MALE,
            prefer_gender=PreferGender.FEMALE,
            description="d1",
        ),
        UserEntity(
            telegram_id=2,
            name="u2",
            age=19,
            latitude=11.0,
            longitude=21.0,
            gender=Gender.FEMALE,
            prefer_gender=PreferGender.MALE,
            description="d2",
        ),
        UserEntity(
            telegram_id=3,
            name="u3",
            age=20,
            latitude=12.0,
            longitude=22.0,
            gender=Gender.FEMALE,
            prefer_gender=PreferGender.MALE,
            description="d3",
        ),
    ]


@pytest.mark.asyncio
async def test_swipe_filter_filters_out_swiped(candidates):
    swipe_repo = AsyncMock()
    swipe_repo.get_swiped_user_ids.return_value = [2]

    service = SwipeFilterService(swipe_repo=swipe_repo)

    result = await service.filter(user_id=999, candidates=candidates)

    assert [u.telegram_id for u in result] == [1, 3]
    swipe_repo.get_swiped_user_ids.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_swipe_filter_returns_all_when_no_swipes(candidates):
    swipe_repo = AsyncMock()
    swipe_repo.get_swiped_user_ids.return_value = []

    service = SwipeFilterService(swipe_repo=swipe_repo)

    result = await service.filter(user_id=999, candidates=candidates)

    assert result == candidates
    swipe_repo.get_swiped_user_ids.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_swipe_filter_returns_empty_when_all_swiped(candidates):
    swipe_repo = AsyncMock()
    swipe_repo.get_swiped_user_ids.return_value = [1, 2, 3]

    service = SwipeFilterService(swipe_repo=swipe_repo)

    result = await service.filter(user_id=999, candidates=candidates)

    assert result == []
    swipe_repo.get_swiped_user_ids.assert_awaited_once_with(999)
