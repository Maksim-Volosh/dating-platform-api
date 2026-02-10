from unittest.mock import AsyncMock

import pytest

from app.application.services import AIProfileAnalyzeService
from app.domain.entities import Gender, PreferGender, UserEntity


@pytest.fixture
def user() -> UserEntity:
    return UserEntity(
        telegram_id=1,
        name="Maks",
        age=22,
        latitude=10.0,
        longitude=20.0,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="Люблю кофе, прогулки и мемы про питон.",
    )


def test_format_message_contains_required_sections_and_user_fields(user):
    service = AIProfileAnalyzeService(ai_repo=AsyncMock())

    msg = service._format_message_by_user(user)

    assert "Ты анализируешь анкету пользователя" in msg
    assert "Плюсы:" in msg
    assert "Минусы:" in msg
    assert "РОВНО 3 плюса" in msg
    assert "РОВНО 2 минуса" in msg
    assert "С эмодзи" in msg

    assert f"Имя: {user.name}" in msg
    assert f"Описание: {user.description}" in msg


@pytest.mark.asyncio
async def test_analyze_calls_repo_complete_with_formatted_message(user):
    ai_repo = AsyncMock()
    ai_repo.complete.return_value = "Плюсы: ... Минусы: ... 🙂"

    service = AIProfileAnalyzeService(ai_repo=ai_repo)

    result = await service.analyze(user)

    assert result == "Плюсы: ... Минусы: ... 🙂"
    ai_repo.complete.assert_awaited_once()

    sent_message = ai_repo.complete.await_args[0][0]
    assert isinstance(sent_message, str)
    assert f"Имя: {user.name}" in sent_message
    assert f"Описание: {user.description}" in sent_message
    assert "Формат ответа:" in sent_message


@pytest.mark.asyncio
async def test_analyze_returns_none_when_repo_returns_none(user):
    ai_repo = AsyncMock()
    ai_repo.complete.return_value = None

    service = AIProfileAnalyzeService(ai_repo=ai_repo)

    result = await service.analyze(user)

    assert result is None
    ai_repo.complete.assert_awaited_once()

