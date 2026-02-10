from unittest.mock import AsyncMock

import pytest

from app.application.services import InboxOnSwipeService
from app.core.config import settings
from app.domain.entities import InboxSwipe


@pytest.fixture
def swipe_match() -> InboxSwipe:
    return InboxSwipe(
        from_user_id=1,
        from_user_id_decision=True,
        to_user_id=2,
        to_user_id_decision=True,
    )


@pytest.fixture
def swipe_incoming() -> InboxSwipe:
    return InboxSwipe(
        from_user_id=1,
        from_user_id_decision=True,
        to_user_id=2,
        to_user_id_decision=False,
    )


@pytest.fixture
def swipe_incoming_none() -> InboxSwipe:
    return InboxSwipe(
        from_user_id=1,
        from_user_id_decision=None,
        to_user_id=2,
        to_user_id_decision=None,
    )


@pytest.mark.asyncio
async def test_create_inbox_item_adds_match_when_decision_true(swipe_match):
    inbox_cache = AsyncMock()
    inbox_cache.add_match.return_value = None
    inbox_cache.add_incoming.return_value = None

    service = InboxOnSwipeService(inbox_cache=inbox_cache)

    await service.create_inbox_item(swipe_match)

    inbox_cache.add_match.assert_awaited_once_with(
        swipe_match.to_user_id,
        swipe_match.from_user_id,
        timeout=settings.inbox.timeout,
    )
    inbox_cache.add_incoming.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_inbox_item_adds_incoming_when_decision_false(swipe_incoming):
    inbox_cache = AsyncMock()
    inbox_cache.add_match.return_value = None
    inbox_cache.add_incoming.return_value = None

    service = InboxOnSwipeService(inbox_cache=inbox_cache)

    await service.create_inbox_item(swipe_incoming)

    inbox_cache.add_incoming.assert_awaited_once_with(
        swipe_incoming.to_user_id,
        swipe_incoming.from_user_id,
        timeout=settings.inbox.timeout,
    )
    inbox_cache.add_match.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_inbox_item_adds_incoming_when_decision_none(swipe_incoming_none):
    inbox_cache = AsyncMock()
    inbox_cache.add_match.return_value = None
    inbox_cache.add_incoming.return_value = None

    service = InboxOnSwipeService(inbox_cache=inbox_cache)

    await service.create_inbox_item(swipe_incoming_none)

    inbox_cache.add_incoming.assert_awaited_once_with(
        swipe_incoming_none.to_user_id,
        swipe_incoming_none.from_user_id,
        timeout=settings.inbox.timeout,
    )
    inbox_cache.add_match.assert_not_awaited()


@pytest.mark.asyncio
async def test__is_match_returns_true_only_for_true(swipe_match, swipe_incoming, swipe_incoming_none):
    service = InboxOnSwipeService(inbox_cache=AsyncMock())

    assert await service._is_match(swipe_match) is True
    assert await service._is_match(swipe_incoming) is False
    assert await service._is_match(swipe_incoming_none) is False
