import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

# Modelos gratuitos disponíveis no Opencode ZEN
ZEN_MODELS = [
    ModelInfo(name="nemotron-3-ultra-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="llama-3.3-70b-versatile", loaded=False, provider="opencode-zen"),
    ModelInfo(name="gemma-2-9b-it", loaded=False, provider="opencode-zen"),
]


class OpencodeZenProvider(BaseProvider):
    """Provider Opencode ZEN (gratuito)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://opencode.ai/zen/v1"

    @property
    def name(self) -> str:
        return "opencode-zen"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def list_models(self) -> list[ModelInfo]:
        """Retorna modelos conhecidos do Opencode ZEN."""
        return ZEN_MODELS.copy()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model or "nemotron-3-ultra-free",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "text-embedding-3-small",
                    "input": text,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
