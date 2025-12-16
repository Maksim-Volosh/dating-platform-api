from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    
class PreferGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    ANYONE = "anyone"

@dataclass
class UserEntity:
    telegram_id: int
    name: str
    age: int
    city: str
    gender: Gender
    prefer_gender: PreferGender
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