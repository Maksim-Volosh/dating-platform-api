from abc import ABC, abstractmethod

from app.domain.entities import InboxItem


class IInboxCache(ABC):
    @abstractmethod
    async def add_incoming(self, owner_id: int, candidate_id: int, timeout=None):
        raise NotImplementedError

    @abstractmethod
    async def add_match(self, owner_id: int, candidate_id: int, timeout=None):
        raise NotImplementedError

    @abstractmethod
    async def peek(self, owner_id: int) -> InboxItem | None:
        raise NotImplementedError

    @abstractmethod
    async def ack(self, owner_id: int, candidate_id: int):
        raise NotImplementedError

    @abstractmethod
    async def count(self, owner_id: int):
        raise NotImplementedError
