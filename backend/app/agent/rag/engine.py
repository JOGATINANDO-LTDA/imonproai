import logging

from app.agent.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


class RAGEngine:
    """Engine RAG para recuperação e geração aumentada."""

    def __init__(self, provider_registry: ProviderRegistry):
        self.registry = provider_registry

    async def retrieve(self, query: str, tenant_id: str, top_k: int = 4) -> list[dict]:
        logger.info(f"RAG retrieve: query={query[:50]}..., tenant={tenant_id}")
        return []

    async def generate(
        self,
        query: str,
        context: list[dict],
        system_prompt: str | None = None,
    ) -> str:
        context_text = "\n".join([c.get("content", "") for c in context])
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append(
            {
                "role": "user",
                "content": f"Contexto:\n{context_text}\n\nPergunta: {query}",
            }
        )
        response = await self.registry.chat(messages)
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")

    async def query(
        self,
        query: str,
        tenant_id: str,
        system_prompt: str | None = None,
    ) -> dict:
        context = await self.retrieve(query, tenant_id)
        answer = await self.generate(query, context, system_prompt)
        return {
            "answer": answer,
            "sources": context,
            "query": query,
        }
