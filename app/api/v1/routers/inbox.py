from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.inbox import CurrentInboxItemResponse, InboxItemCountResponse, AckInboxItemRequest
from app.core.containers.inbox import get_inbox_use_case
from app.domain.entities import InboxItem
from app.domain.exceptions import InboxItemNotFound
from app.application.use_cases import InboxUseCase

router = APIRouter(prefix="/inbox", tags=["Inbox"])


@router.get("/current/{owner_id}", status_code=200)
async def get_next_inbox_item(
    owner_id: int,
    use_case: InboxUseCase = Depends(get_inbox_use_case)
) -> CurrentInboxItemResponse:
    try:
        entity: InboxItem = await use_case.peek_current(owner_id)
    except InboxItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    
    return CurrentInboxItemResponse(
        candidate_id=entity.candidate_id,
        type=entity.type
    )

@router.get("/count/{owner_id}", status_code=200)
async def get_inbox_count(
    owner_id: int,
    use_case: InboxUseCase = Depends(get_inbox_use_case)
) -> InboxItemCountResponse:
    count = await use_case.get_count(owner_id)
    
    return InboxItemCountResponse(count=count)

@router.post("/ack/{owner_id}", status_code=204)
async def ackward_inbox_item(
    owner_id: int,
    body: AckInboxItemRequest,
    use_case: InboxUseCase = Depends(get_inbox_use_case)
):
    await use_case.ack_item(owner_id, body.candidate_id)