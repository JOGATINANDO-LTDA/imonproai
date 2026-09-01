from app.agent.rag.engine import RAGEngine
from app.agent.providers.registry import ProviderRegistry


def test_rag_engine_init():
    registry = ProviderRegistry()
    rag = RAGEngine(registry)
    assert rag.registry is registry
