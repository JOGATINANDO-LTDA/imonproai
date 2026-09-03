import uuid

import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

# Modelos conhecidos do Opencode Go (fallback se API indisponível)
GO_MODELS = [
    ModelInfo(name="deepseek-v4-flash", loaded=False, provider="opencode-go"),
    ModelInfo(name="deepseek-v4-pro", loaded=False, provider="opencode-go"),
    ModelInfo(name="glm-5.3-flash", loaded=False, provider="opencode-go"),
    ModelInfo(name="glm-5.3", loaded=False, provider="opencode-go"),
    ModelInfo(name="glm-5.2", loaded=False, provider="opencode-go"),
    ModelInfo(name="mimo-v2.5", loaded=False, provider="opencode-go"),
    ModelInfo(name="mimo-v2.5-pro", loaded=False, provider="opencode-go"),
    ModelInfo(name="minimax-m3", loaded=False, provider="opencode-go"),
    ModelInfo(name="minimax-m2.7", loaded=False, provider="opencode-go"),
    ModelInfo(name="kimi-k3", loaded=False, provider="opencode-go"),
    ModelInfo(name="kimi-k2.7-code", loaded=False, provider="opencode-go"),
    ModelInfo(name="qwen3.8-flash", loaded=False, provider="opencode-go"),
    ModelInfo(name="qwen3.7-plus", loaded=False, provider="opencode-go"),
    ModelInfo(name="grok-4.6", loaded=False, provider="opencode-go"),
    ModelInfo(name="gpt-5.6-luna", loaded=False, provider="opencode-go"),
]


class OpenCodeGoProvider(BaseProvider):
    """Provider Opencode Go ($10/mês, 25+ modelos de programação)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://opencode.ai/zen/go/v1"
        self._session_id = str(uuid.uuid4())

    @property
    def name(self) -> str:
        return "opencode-go"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def list_models(self) -> list[ModelInfo]:
        """Busca modelos da API do Opencode Go."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "x-opencode-session": self._session_id,
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()

            models = []
            for m in data.get("data", []):
                model_id = m.get("id", "")
                models.append(ModelInfo(
                    name=model_id,
                    loaded=False,
                    provider="opencode-go",
                ))

            return models if models else GO_MODELS.copy()
        except Exception:
            return GO_MODELS.copy()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "x-opencode-session": self._session_id,
                },
                json={
                    "model": model or "deepseek-v4-flash",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Opencode Go não suporta embeddings")
