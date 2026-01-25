from pydantic import BaseModel

from app.domain.entities.inbox import InboxItemType


class CurrentInboxItemResponse(BaseModel):
    candidate_id: int
    type: InboxItemType


class InboxItemCountResponse(BaseModel):
    count: int


class AckInboxItemRequest(BaseModel):
    candidate_id: int
