from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Provider base para IA."""

    @abstractmethod
    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        pass

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        pass
