from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Informações sobre um modelo disponível."""
    name: str
    loaded: bool = False
    size_bytes: int | None = None
    provider: str = ""
    instance_id: str | None = None


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

    @property
    def supports_model_management(self) -> bool:
        """Se o provider suporta load/unload de modelos."""
        return False

    async def list_models(self) -> list[ModelInfo]:
        """Lista modelos disponíveis no provider."""
        return []

    async def load_model(self, model: str, **kwargs) -> dict:
        """Carrega um modelo na memória. Retorna status."""
        raise NotImplementedError(f"{self.name} não suporta load/unload")

    async def unload_model(self, instance_id: str) -> dict:
        """Descarrega um modelo da memória. Retorna status."""
        raise NotImplementedError(f"{self.name} não suporta load/unload")

    async def is_model_loaded(self, model: str) -> bool:
        """Verifica se um modelo específico está carregado."""
        return False
