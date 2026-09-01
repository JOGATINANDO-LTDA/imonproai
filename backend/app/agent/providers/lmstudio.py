import httpx

from app.agent.providers.base import BaseProvider


class LMStudioProvider(BaseProvider):
    """Provider local via LMStudio."""

    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.base_url = base_url

    @property
    def name(self) -> str:
        return "lmstudio"

    @property
    def is_available(self) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/models", timeout=2.0)
            return response.status_code == 200
        except Exception:
            return False

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": model or "qwen3.5-9b-deepseek-v4-flash",
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
                json={
                    "model": "nomic-embed-text-v1.5",
                    "input": text,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
