from typing import List, Optional

from pydantic import BaseModel

from app.infrastructure.models.users import Gender, PreferGender

class UserResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserCreateRequest(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserCreateResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender
    
class UserUpdateRequest(BaseModel):
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender
    
class UserUpdateResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

