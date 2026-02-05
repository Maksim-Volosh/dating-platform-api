import os

from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                    AsyncOpenAI, AuthenticationError, BadRequestError,
                    NotFoundError, PermissionDeniedError, RateLimitError)

from app.domain.interfaces import IAIClientRepository


class OpenRouterClient(IAIClientRepository):
    def __init__(self, client: AsyncOpenAI) -> None:
        self._client = client

    async def complete(self, message: str, model: str = "openrouter/free", temperature: float = 0.7) -> str | None: 
        try:
            resp = await self._client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
            )
            return resp.choices[0].message.content or None

        except APITimeoutError:
            return None
        except APIConnectionError:
            return None
        except RateLimitError:
            return None
        
        except (AuthenticationError, PermissionDeniedError, BadRequestError, NotFoundError):
            raise
        
        except APIStatusError as e:
            if 500 <= e.status_code < 600:
                return None
            raise

