import asyncio

from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                    AsyncOpenAI, AuthenticationError, BadRequestError,
                    NotFoundError, PermissionDeniedError, RateLimitError)

from app.domain.interfaces import IAIClientRepository


class OpenRouterClient(IAIClientRepository):
    def __init__(self, client: AsyncOpenAI, timeout: int) -> None:
        self._client = client
        self.timeout = timeout

    async def complete(self, message: str, model: str = "arcee-ai/trinity-large-preview:free", temperature: float = 0.7) -> str | None: 
        try:
            resp = await asyncio.wait_for(
                self._client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    temperature=temperature,
                ),
                timeout=self.timeout,
            )
            return resp.choices[0].message.content or None

        except (asyncio.TimeoutError, APITimeoutError):
            return None
        # except APIConnectionError:
        #     return None
        # except RateLimitError:
        #     return None
        # except NotFoundError:
        #     return None
        
        # except (AuthenticationError, PermissionDeniedError, BadRequestError):
        #     raise
        
        except APIStatusError as e:
            if 500 <= e.status_code < 600:
                return None
            raise

