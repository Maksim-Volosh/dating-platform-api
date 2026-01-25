from typing import Any
from app.infrastructure.api_client import APIClient
from app.infrastructure.errors import HTTPError


class DeckService:
    def __init__(self, api: APIClient) -> None:
        self._api = api

    async def get_next_user(self, telegram_id: int) -> Any | None:
        try:
            user_data = await self._api.post(
                f"/decks/next/{telegram_id}", expected_status=200
            )
        except HTTPError as e:
            if e.status == 404:
                return None
            else:
                raise

        return user_data
