from dataclasses import dataclass


@dataclass
class LikeEntity:
    liker_id: int
    more: int