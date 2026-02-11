import asyncio
from typing import Any

import aiohttp
from config import API_KEY, API_URL

from app.infrastructure.errors import HTTPError

JsonType = dict | list | None


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 50,
        retries: int = 2,
    ):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._retries = retries
        self._session: aiohttp.ClientSession | None = None

    async def start(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=self._timeout,
                headers={"x-api-key": self._api_key},
            )

    async def close(self):
        if self._session:
            await self._session.close()

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: JsonType = None,
        expected_status: int = 200,
    ) -> Any:
        if not self._session:
            raise RuntimeError("HTTPClient not started")

        url = f"{self._base_url}{path}"

        for attempt in range(self._retries + 1):
            try:
                async with self._session.request(
                    method,
                    url,
                    json=json,
                ) as resp:
                    if resp.status != expected_status:
                        text = await resp.text()
                        raise HTTPError(resp.status, text)

                    if expected_status == 204:
                        return None

                    return await resp.json()

            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt >= self._retries:
                    raise
                await asyncio.sleep(0.2 * (attempt + 1))


http = HTTPClient(
    base_url=API_URL,
    api_key=API_KEY,
)
