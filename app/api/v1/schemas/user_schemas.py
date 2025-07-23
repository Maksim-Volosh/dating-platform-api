from typing import List, Optional

from pydantic import BaseModel

from app.infrastructure.models.users import Gender, PreferGender


class UserCreate(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserReadResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender
    
class UserUpdateRequest(UserCreate):
    ...
    
class UserUpdateResponse(UserCreate):
    ...