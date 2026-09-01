import httpx

from app.agent.providers.base import BaseProvider


class GroqProvider(BaseProvider):
    """Provider Groq (gratuito, alta velocidade)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"

    @property
    def name(self) -> str:
        return "groq"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model or "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Groq não suporta embeddings")
