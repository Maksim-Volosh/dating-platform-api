from dataclasses import dataclass
from typing import Optional

@dataclass
class UserEntity:
    telegram_id: int
    name: str
    age: int
    city: str
    gender: str
    prefer_gender: str
    description: Optional[str] = None