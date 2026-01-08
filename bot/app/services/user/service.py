from typing import Any

from app.infrastructure.api_client import APIClient
from app.infrastructure.errors import HTTPError

GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
}
PREFER_GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
    "Неважно": "anyone",
}

class UserService:
    def __init__(self, api: APIClient) -> None:
        self._api = api
        
    async def get_user(self, telegram_id: int) -> None | Any:
        try:
            data = await self._api.get(f"/users/{telegram_id}")
        except HTTPError as e:
            if e.status == 404:
                return None
            else:
                raise
        return data
    
    async def create_user_profile(self, data: dict, telegram_id: int):
        user_payload = {
            "telegram_id": telegram_id,
            "name": data["name"],
            "age": int(data["age"]),
            "city": data["city"],
            "description": data["description"],
            "gender": GENDER_MAP[data["gender"]],
            "prefer_gender": PREFER_GENDER_MAP[data["prefer_gender"]],
        }
        
        return await self._api.post(f"/users/", json=user_payload)
    
    async def update_user_profile(self, data: dict, telegram_id: int):
        user_payload = {
            "name": data["name"],
            "age": int(data["age"]),
            "city": data["city"],
            "description": data["description"],
            "gender": GENDER_MAP[data["gender"]],
            "prefer_gender": PREFER_GENDER_MAP[data["prefer_gender"]],
        }
        
        return await self._api.put(f"/users/{telegram_id}/", json=user_payload)

    async def update_description(self, telegram_id: int, description: str):
        description_payload = {
            "description": description
        }

        return await self._api.patch(f"/users/{telegram_id}/description/", json=description_payload)