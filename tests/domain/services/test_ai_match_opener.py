from unittest.mock import AsyncMock

import pytest

from app.application.services.ai_match_opener import AIMatchOpenerService
from app.domain.entities import Gender, PreferGender, UserEntity


@pytest.fixture
def liker_user() -> UserEntity:
    return UserEntity(
        telegram_id=1,
        name="Maks",
        age=22,
        latitude=10.0,
        longitude=20.0,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="Люблю кофе и прогулки",
    )


@pytest.fixture
def candidate_user() -> UserEntity:
    return UserEntity(
        telegram_id=2,
        name="Anna",
        age=21,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="Книги, музеи, немного сарказма",
    )


def test_format_message_contains_user_fields(liker_user, candidate_user):
    service = AIMatchOpenerService(ai_repo=AsyncMock())

    msg = service._format_message_by_users(liker_user, candidate_user)

    assert "первое сообщение" in msg
    assert "Вариант 1:" in msg
    assert "Вариант 2:" in msg
    assert "Вариант 3:" in msg

    assert f"Имя: {liker_user.name}" in msg
    assert f"Описание: {liker_user.description}" in msg
    assert f"Возраст: {liker_user.age}" in msg
    assert f"Гендер: {liker_user.gender}" in msg

    assert f"Имя: {candidate_user.name}" in msg
    assert f"Описание: {candidate_user.description}" in msg
    assert f"Возраст: {candidate_user.age}" in msg
    assert f"Гендер: {candidate_user.gender}" in msg


@pytest.mark.asyncio
async def test_generate_calls_repo_complete_with_formatted_message(liker_user, candidate_user):
    ai_repo = AsyncMock()
    ai_repo.complete.return_value = "Вариант 1: ...\nВариант 2: ...\nВариант 3: ..."

    service = AIMatchOpenerService(ai_repo=ai_repo)

    result = await service.generate(liker_user, candidate_user)

    assert result == ai_repo.complete.return_value
    ai_repo.complete.assert_awaited_once()

    sent_message = ai_repo.complete.await_args[0][0]
    assert isinstance(sent_message, str)

    assert f"Имя: {liker_user.name}" in sent_message
    assert f"Имя: {candidate_user.name}" in sent_message
    assert "Формат ответа (строго соблюдай):" in sent_message


@pytest.mark.asyncio
async def test_generate_returns_none_when_ai_repo_returns_none(liker_user, candidate_user):
    ai_repo = AsyncMock()
    ai_repo.complete.return_value = None

    service = AIMatchOpenerService(ai_repo=ai_repo)

    result = await service.generate(liker_user, candidate_user)

    assert result is None
    ai_repo.complete.assert_awaited_once()
