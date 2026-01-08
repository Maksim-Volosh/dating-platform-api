from app.infrastructure.api_client import APIClient

class PhotoService:
    def __init__(self, api: APIClient) -> None:
        self._api = api
        
    async def get_user_photos(self, telegram_id: int):
        data = await self._api.get(f"/users/{telegram_id}/photos")
        return data.get("photos", [])
    
    async def create_photos_for_user(self, data: dict, telegram_id: int):
        photo_payload = [
            {"file_id": file_id} for file_id in data["photo_ids"]
        ]
        return await self._api.post(f"/users/{telegram_id}/photos/", json=photo_payload)
    
    async def update_photos_for_user(self, data: dict, telegram_id: int):
        photo_payload = [
            {"file_id": file_id} for file_id in data["photo_ids"]
        ]
        return await self._api.put(f"/users/{telegram_id}/photos/", json=photo_payload, expected_status=201)