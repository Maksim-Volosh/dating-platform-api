from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.inbox import InboxUseCase
from app.domain.entities import InboxItem, InboxItemType
from app.domain.exceptions import InboxItemNotFound


@pytest.fixture
def inbox_item() -> InboxItem:
    return InboxItem(candidate_id=123, type=InboxItemType.INCOMING)


@pytest.mark.asyncio
async def test_peek_current_returns_item_when_exists(inbox_item):
    cache = AsyncMock()
    cache.peek.return_value = inbox_item

    use_case = InboxUseCase(cache=cache)

    result = await use_case.peek_current(owner_id=1)

    assert result == inbox_item
    cache.peek.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_peek_current_raises_when_empty():
    cache = AsyncMock()
    cache.peek.return_value = None

    use_case = InboxUseCase(cache=cache)

    with pytest.raises(InboxItemNotFound):
        await use_case.peek_current(owner_id=1)

    cache.peek.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_count_returns_value_and_calls_cache():
    cache = AsyncMock()
    cache.count.return_value = 7

    use_case = InboxUseCase(cache=cache)

    result = await use_case.get_count(liked_id=555)

    assert result == 7
    cache.count.assert_awaited_once_with(555)


@pytest.mark.asyncio
async def test_ack_item_calls_cache_ack():
    cache = AsyncMock()
    cache.ack.return_value = None

    use_case = InboxUseCase(cache=cache)

    await use_case.ack_item(owner_id=1, candidate_id=2)

    cache.ack.assert_awaited_once_with(1, 2)
