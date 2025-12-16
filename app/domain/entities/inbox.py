from dataclasses import dataclass
from enum import Enum


class InboxItemType(str, Enum):
    INCOMING = "INCOMING"
    MATCH = "MATCH"

@dataclass
class InboxItem:
    candidate_id: int
    type: InboxItemType
    
@dataclass
class InboxSwipe:
    from_user_id: int
    from_user_id_decision: bool | None
    to_user_id: int
    to_user_id_decision: bool | None