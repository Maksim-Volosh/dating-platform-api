from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.inbox import (
    AckInboxItemRequest,
    CurrentInboxItemResponse,
    InboxItemCountResponse,
)
from app.core.composition.container import Container
from app.core.composition.di import get_container
from app.domain.entities import InboxItem
from app.domain.exceptions import InboxItemNotFound

router = APIRouter(prefix="/inbox", tags=["Inbox"])


@router.get("/current/{owner_id}", status_code=200)
async def get_next_inbox_item(
    owner_id: int, container: Container = Depends(get_container)
) -> CurrentInboxItemResponse:
    try:
        entity: InboxItem = await container.inbox_use_case().peek_current(owner_id)
    except InboxItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)

    return CurrentInboxItemResponse(candidate_id=entity.candidate_id, type=entity.type)


@router.get("/count/{owner_id}", status_code=200)
async def get_inbox_count(
    owner_id: int, container: Container = Depends(get_container)
) -> InboxItemCountResponse:
    count = await container.inbox_use_case().get_count(owner_id)

    return InboxItemCountResponse(count=count)


@router.post("/ack/{owner_id}", status_code=204)
async def ackward_inbox_item(
    owner_id: int,
    body: AckInboxItemRequest,
    container: Container = Depends(get_container),
):
    await container.inbox_use_case().ack_item(owner_id, body.candidate_id)
