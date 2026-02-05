from typing import AsyncGenerator
from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIHelper:
    def __init__(self, base_url: str | None, api_key: str) -> None:
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def dispose(self) -> None:
        await self.client.close()

    async def get_client(self) -> AsyncGenerator[AsyncOpenAI, None]:
        yield self.client


ai_helper = OpenAIHelper(
    base_url=settings.ai.base_url,
    api_key=settings.ai.api_key,
)