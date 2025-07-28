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
    
    def to_dict(self):
        return {
            "telegram_id": self.telegram_id,
            "name": self.name,
            "age": self.age,
            "city": self.city,
            "gender": self.gender,
            "prefer_gender": self.prefer_gender,
            "description": self.description,
        }