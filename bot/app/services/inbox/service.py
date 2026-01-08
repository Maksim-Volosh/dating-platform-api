from app.infrastructure.api_client import APIClient

class InboxService:
    def __init__(self, api: APIClient) -> None:
        self._api = api
        
    async def ack_inbox_item(self, owner_id: int, candidate_id: int):
        return await self._api.post(f"/inbox/ack/{owner_id}", json={"candidate_id": candidate_id}, expected_status=204)
    
    async def get_inbox_count(self, owner_id: int):
        data = await self._api.get(f"/inbox/count/{owner_id}")
        count = data.get("count")
        return count
    
    async def get_next_item(self, owner_id: int):
        return await self._api.get(f"/inbox/current/{owner_id}")