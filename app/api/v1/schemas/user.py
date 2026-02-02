from typing import List, Optional

from pydantic import BaseModel

from app.domain.entities import UserEntity
from app.infrastructure.models.users import Gender, PreferGender


class UserResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    longitude: float
    latitude: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserDistanceResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    distance: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

class UserCreateRequest(BaseModel):
    telegram_id: int
    name: str
    age: int
    longitude: float
    latitude: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

    def to_entity(self) -> UserEntity:
        return UserEntity(**self.model_dump())


class UserCreateResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    longitude: float
    latitude: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender


class UserUpdateRequest(BaseModel):
    name: str
    age: int
    longitude: float
    latitude: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender

    def to_entity(self) -> UserEntity:
        return UserEntity(telegram_id=0, **self.model_dump())


class UserUpdateResponse(BaseModel):
    telegram_id: int
    name: str
    age: int
    longitude: float
    latitude: float
    description: Optional[str]
    gender: Gender
    prefer_gender: PreferGender


class UserUpdateDescriptionRequest(BaseModel):
    description: str
