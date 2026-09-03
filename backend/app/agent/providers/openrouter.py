import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

# Modelos gratuitos conhecidos do OpenRouter (fallback se API indisponível)
OPENROUTER_FREE_MODELS = [
    ModelInfo(name="meta-llama/llama-3.3-70b-instruct:free", loaded=False, provider="openrouter"),
    ModelInfo(name="google/gemma-4-31b-it:free", loaded=False, provider="openrouter"),
    ModelInfo(name="nvidia/nemotron-3-ultra-550b-a55b:free", loaded=False, provider="openrouter"),
    ModelInfo(name="qwen/qwen3-coder:free", loaded=False, provider="openrouter"),
    ModelInfo(name="openai/gpt-oss-120b:free", loaded=False, provider="openrouter"),
    ModelInfo(name="minimax/minimax-m3:free", loaded=False, provider="openrouter"),
    ModelInfo(name="z-ai/glm-5.2:free", loaded=False, provider="openrouter"),
]


class OpenRouterProvider(BaseProvider):
    """Provider OpenRouter (26+ modelos gratuitos, 50 req/dia)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"

    @property
    def name(self) -> str:
        return "openrouter"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def list_models(self) -> list[ModelInfo]:
        """Busca modelos gratuitos da API do OpenRouter."""
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
                pricing = m.get("pricing", {})
                prompt_cost = pricing.get("prompt", "1")
                completion_cost = pricing.get("completion", "1")

                # Incluir modelos gratuitos (preço == "0" ou suffix :free)
                if prompt_cost == "0" and completion_cost == "0":
                    models.append(ModelInfo(
                        name=model_id,
                        loaded=False,
                        provider="openrouter",
                    ))

            return models if models else OPENROUTER_FREE_MODELS.copy()
        except Exception:
            return OPENROUTER_FREE_MODELS.copy()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://imobpro.ai",
                    "X-Title": "ImobPro.ai",
                },
                json={
                    "model": model or "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("OpenRouter não suporta embeddings")
