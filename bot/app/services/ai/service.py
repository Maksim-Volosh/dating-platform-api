from typing import Any
from app.infrastructure.api_client import APIClient
from app.infrastructure.errors import HTTPError


class AIService:
    def __init__(self, api: APIClient) -> None:
        self._api = api

    async def get_ai_profile_analyze(self, telegram_id: int) -> Any | None | bool:
        try:
            result = await self._api.get(f"/ai/profile-analyze/{telegram_id}")
        except HTTPError as e:
            if e.status == 404 or e.status == 503:
                return None
            if e.status == 429:
                return False
            else:
                raise

        return result

    async def get_ai_match_opener(
        self, liker_id: int, candidate_id: int
    ) -> Any | None | bool:
        try:
            result = await self._api.get(
                f"/ai/match-opener/{liker_id}?candidate_id={candidate_id}"
            )
        except HTTPError as e:
            if e.status == 404 or e.status == 503:
                return None
            if e.status == 429:
                return False
            else:
                raise

        return result
