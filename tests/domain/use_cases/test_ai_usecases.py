from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.ai import (AIMatchOpenerUseCase,
                                          AIProfileAnalyzeUseCase)
from app.domain.entities import Gender, PreferGender, UserEntity
from app.domain.exceptions import AIUnavailableError, UserNotFoundById


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


# -------------------------------
# AIProfileAnalyzeUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_ai_profile_analyze_success(fake_user):
    user_repo = AsyncMock()
    user_repo.get_by_id.return_value = fake_user

    ai_service = AsyncMock()
    ai_service.analyze.return_value = "analysis text"

    use_case = AIProfileAnalyzeUseCase(ai_analyze_service=ai_service, user_repo=user_repo)

    result = await use_case.execute(telegram_id=fake_user.telegram_id)

    assert result == "analysis text"
    user_repo.get_by_id.assert_awaited_once_with(fake_user.telegram_id)
    ai_service.analyze.assert_awaited_once_with(fake_user)


@pytest.mark.asyncio
async def test_ai_profile_analyze_user_not_found_raises():
    user_repo = AsyncMock()
    user_repo.get_by_id.return_value = None

    ai_service = AsyncMock()

    use_case = AIProfileAnalyzeUseCase(ai_analyze_service=ai_service, user_repo=user_repo)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(telegram_id=123)

    user_repo.get_by_id.assert_awaited_once_with(123)
    ai_service.analyze.assert_not_awaited()


@pytest.mark.asyncio
async def test_ai_profile_analyze_ai_unavailable_raises(fake_user):
    user_repo = AsyncMock()
    user_repo.get_by_id.return_value = fake_user

    ai_service = AsyncMock()
    ai_service.analyze.return_value = None

    use_case = AIProfileAnalyzeUseCase(ai_analyze_service=ai_service, user_repo=user_repo)

    with pytest.raises(AIUnavailableError):
        await use_case.execute(telegram_id=fake_user.telegram_id)

    user_repo.get_by_id.assert_awaited_once_with(fake_user.telegram_id)
    ai_service.analyze.assert_awaited_once_with(fake_user)


# -------------------------------
# AIMatchOpenerUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_ai_match_opener_success(fake_user):
    liker = fake_user
    candidate = UserEntity(
        telegram_id=2,
        name="cand",
        age=19,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="candidate",
    )

    user_repo = AsyncMock()
    # два вызова get_by_id: сначала liker, потом candidate
    user_repo.get_by_id.side_effect = [liker, candidate]

    ai_service = AsyncMock()
    ai_service.generate.return_value = "opener text"

    use_case = AIMatchOpenerUseCase(ai_opener_service=ai_service, user_repo=user_repo)

    result = await use_case.execute(liker_id=liker.telegram_id, candidate_id=candidate.telegram_id)

    assert result == "opener text"
    assert user_repo.get_by_id.await_count == 2
    user_repo.get_by_id.assert_any_await(liker.telegram_id)
    user_repo.get_by_id.assert_any_await(candidate.telegram_id)
    ai_service.generate.assert_awaited_once_with(liker, candidate)


@pytest.mark.asyncio
async def test_ai_match_opener_user_not_found_raises_when_liker_missing(fake_user):
    candidate = UserEntity(
        telegram_id=2,
        name="cand",
        age=19,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="candidate",
    )

    user_repo = AsyncMock()
    user_repo.get_by_id.side_effect = [None, candidate]

    ai_service = AsyncMock()

    use_case = AIMatchOpenerUseCase(ai_opener_service=ai_service, user_repo=user_repo)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(liker_id=1, candidate_id=2)

    assert user_repo.get_by_id.await_count == 2
    ai_service.generate.assert_not_awaited()


@pytest.mark.asyncio
async def test_ai_match_opener_user_not_found_raises_when_candidate_missing(fake_user):
    user_repo = AsyncMock()
    user_repo.get_by_id.side_effect = [fake_user, None]

    ai_service = AsyncMock()

    use_case = AIMatchOpenerUseCase(ai_opener_service=ai_service, user_repo=user_repo)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(liker_id=fake_user.telegram_id, candidate_id=999)

    assert user_repo.get_by_id.await_count == 2
    ai_service.generate.assert_not_awaited()


@pytest.mark.asyncio
async def test_ai_match_opener_ai_unavailable_raises(fake_user):
    liker = fake_user
    candidate = UserEntity(
        telegram_id=2,
        name="cand",
        age=19,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="candidate",
    )

    user_repo = AsyncMock()
    user_repo.get_by_id.side_effect = [liker, candidate]

    ai_service = AsyncMock()
    ai_service.generate.return_value = None

    use_case = AIMatchOpenerUseCase(ai_opener_service=ai_service, user_repo=user_repo)

    with pytest.raises(AIUnavailableError):
        await use_case.execute(liker_id=liker.telegram_id, candidate_id=candidate.telegram_id)

    ai_service.generate.assert_awaited_once_with(liker, candidate)
