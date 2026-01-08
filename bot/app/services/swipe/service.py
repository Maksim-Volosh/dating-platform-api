from app.infrastructure.api_client import APIClient

class SwipeService:
    def __init__(self, api: APIClient) -> None:
        self._api = api
        
    async def create_swipe(self, liker_id: int, liked_id: int, decision: bool):
        swipe_payload = {
            "liker_id": liker_id,
            "liked_id": liked_id,
            "decision": decision
        }
        
        return await self._api.post(f"/swipes/", json=swipe_payload)