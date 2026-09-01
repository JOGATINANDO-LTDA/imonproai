from app.agent.providers.base import BaseProvider
from app.agent.providers.registry import ProviderRegistry


class MockProvider(BaseProvider):
    def __init__(self, name: str = "mock"):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_available(self) -> bool:
        return True

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        return {"choices": [{"message": {"content": "mock response"}}]}

    async def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_provider_registry_register():
    registry = ProviderRegistry()
    provider = MockProvider()
    registry.register(provider)
    assert "mock" in registry._providers


def test_provider_registry_get():
    registry = ProviderRegistry()
    provider = MockProvider()
    registry.register(provider)
    assert registry.get("mock") is provider
    assert registry.get("nonexistent") is None


def test_provider_registry_available():
    registry = ProviderRegistry()
    provider = MockProvider()
    registry.register(provider)
    assert "mock" in registry.available_providers
