from dataclasses import dataclass
from typing import Optional


@dataclass
class SwipeEntity:
    liker_id: int
    liked_id: int
    decision: bool
    
@dataclass
class NormalizedSwipeEntity:
    user1_id: int
    user2_id: int
    decision: bool
    liker_is_user1: bool