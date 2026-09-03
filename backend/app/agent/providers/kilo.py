import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

# Modelos gratuitos conhecidos do Kilo Gateway (fallback se API indisponível)
KILO_FREE_MODELS = [
    ModelInfo(name="openrouter/free", loaded=False, provider="kilo"),
    ModelInfo(name="nvidia/nemotron-3-ultra-550b-a55b:free", loaded=False, provider="kilo"),
    ModelInfo(name="google/gemma-4-26b-a4b-it:free", loaded=False, provider="kilo"),
    ModelInfo(name="poolside/laguna-s-2.1:free", loaded=False, provider="kilo"),
    ModelInfo(name="z-ai/glm-5:free", loaded=False, provider="kilo"),
    ModelInfo(name="minimax/minimax-m2.1:free", loaded=False, provider="kilo"),
]


class KiloProvider(BaseProvider):
    """Provider Kilo Gateway (8+ modelos gratuitos, 200 req/hr)."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.base_url = "https://api.kilo.ai/api/gateway"

    @property
    def name(self) -> str:
        return "kilo"

    @property
    def is_available(self) -> bool:
        # Kilo permite acesso anônimo para modelos free
        return True

    async def list_models(self) -> list[ModelInfo]:
        """Busca modelos gratuitos da API do Kilo Gateway."""
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()

            models = []
            for m in data.get("data", []):
                model_id = m.get("id", "")
                # Incluir modelos com suffix :free
                if model_id.endswith(":free") or model_id == "openrouter/free":
                    models.append(ModelInfo(
                        name=model_id,
                        loaded=False,
                        provider="kilo",
                    ))

            return models if models else KILO_FREE_MODELS.copy()
        except Exception:
            return KILO_FREE_MODELS.copy()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": model or "openrouter/free",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Kilo Gateway não suporta embeddings")
