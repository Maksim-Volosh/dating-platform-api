from typing import List, Optional

from pydantic import BaseModel

from app.infrastructure.models.users import Gender, PreferGender


class UserCreateRequest(BaseModel):
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserCreateResponse(BaseModel):
    id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserReadResponse(BaseModel):
    id: int
    name: str
    age: int
    city: str
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender
    
class UserUpdateRequest(UserCreateRequest):
    ...
    
class UserUpdateResponse(UserCreateResponse):
    ...