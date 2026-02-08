from abc import ABC, abstractmethod


class IAIClientRepository(ABC):
    @abstractmethod
    async def complete(
        self, message: str, model: str = "openrouter/free", temperature: float = 0.7
    ) -> str | None:
        raise NotImplementedError
