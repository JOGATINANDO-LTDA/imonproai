import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

# Modelos gratuitos do Opencode ZEN (fallback se API indisponível)
ZEN_FREE_MODELS = [
    ModelInfo(name="mimo-v2.5-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="ling-3.0-flash-fin-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="nemotron-3-ultra-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="nemotron-3.5-lightning-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="big-pickle", loaded=False, provider="opencode-zen"),
    ModelInfo(name="muse-spark-1.3-contributor-free", loaded=False, provider="opencode-zen"),
    ModelInfo(name="muse-spark-1.2-contributor-free", loaded=False, provider="opencode-zen"),
]

# Modelos pagos conhecidos (fallback)
ZEN_PAID_MODELS = [
    ModelInfo(name="deepseek-v4-flash", loaded=False, provider="opencode-zen"),
    ModelInfo(name="deepseek-v4-pro", loaded=False, provider="opencode-zen"),
    ModelInfo(name="glm-5.2", loaded=False, provider="opencode-zen"),
    ModelInfo(name="minimax-m3", loaded=False, provider="opencode-zen"),
    ModelInfo(name="kimi-k3", loaded=False, provider="opencode-zen"),
]


class OpencodeZenProvider(BaseProvider):
    """Provider Opencode ZEN (7+ modelos gratuitos, pay-per-token)."""

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
        """Busca modelos da API do Opencode ZEN."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
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
                    provider="opencode-zen",
                ))

            return models if models else ZEN_FREE_MODELS.copy() + ZEN_PAID_MODELS.copy()
        except Exception:
            return ZEN_FREE_MODELS.copy() + ZEN_PAID_MODELS.copy()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model or "mimo-v2.5-free",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Opencode ZEN não suporta embeddings")
