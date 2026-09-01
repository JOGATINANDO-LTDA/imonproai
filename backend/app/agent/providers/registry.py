import logging

from app.agent.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """Registry de providers de IA com fallback chain."""

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        self._providers[provider.name] = provider
        logger.info(f"Provider registrado: {provider.name}")

    def get(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    @property
    def available_providers(self) -> list[str]:
        return [name for name, p in self._providers.items() if p.is_available]

    async def chat(
        self,
        messages: list[dict],
        model: str | None = None,
        provider_name: str | None = None,
    ) -> dict:
        if provider_name:
            provider = self._providers.get(provider_name)
            if provider and provider.is_available:
                return await provider.chat(messages, model)
            raise ValueError(f"Provider {provider_name} não disponível")

        for name, provider in self._providers.items():
            if provider.is_available:
                try:
                    return await provider.chat(messages, model)
                except Exception as e:
                    logger.warning(f"Provider {name} falhou: {e}")
                    continue

        raise RuntimeError("Todos os providers falharam")

    async def embed(self, text: str, provider_name: str | None = None) -> list[float]:
        if provider_name:
            provider = self._providers.get(provider_name)
            if provider and provider.is_available:
                return await provider.embed(text)
            raise ValueError(f"Provider {provider_name} não disponível")

        for name, provider in self._providers.items():
            if provider.is_available:
                try:
                    return await provider.embed(text)
                except Exception as e:
                    logger.warning(f"Provider {name} falhou no embed: {e}")
                    continue

        raise RuntimeError("Todos os providers falharam no embed")
