from dataclasses import dataclass


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


@dataclass
class FullSwipeEntity:
    user1_id: int
    user1_decision: bool | None
    user2_id: int
    user2_decision: bool | None
