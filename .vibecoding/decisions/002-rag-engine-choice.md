# ADR-002: Engine RAG Híbrida (LlamaIndex + LangChain)

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa de RAG para:
- Buscar informações de imóveis
- Responder perguntas sobre documentos
- Fornecer contexto ao agente comercial

O RAG precisa de:
- Controle fino sobre chunking
- Hybrid search (vector + keyword)
- Reranking para qualidade
- Evals para medir qualidade
- Observabilidade via Langfuse

## Decisão

Usar **LlamaIndex** para RAG core + **LangChain** para orquestração:

- **LlamaIndex**: Data ingestion, indexing, hybrid search, reranking
- **LangChain**: Chains, agents, integrações, tracing
- **pgvector**: Vector store unificado

## Justificativa

### Por que híbrido?

| Capacidade | LlamaIndex | LangChain | Híbrido |
|-----------|-----------|----------|---------|
| RAG depth | Excelente | Bom | Melhor |
| Agents | Limitado | Excelente | Melhor |
| Integrações | Boas | Muitas | Melhor |
| Evals | DeepEval | Rigor | Rigor |
| Tracing | Langfuse | Langfuse | Langfuse |

### LlamaIndex para RAG

- Controle fino sobre chunking (recursive, semantic, auto-merging)
- Hybrid search nativo (vector + BM25)
- Reranking com cross-encoder
- Evals integrados (faithfulness, relevancy, recall)

### LangChain para Orquestração

- LangGraph para state machines
- Integrações com muitos providers
- Langfuse para tracing
- Community ativa

## Implementação

```python
# LlamaIndex para RAG
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pgvector import PgVectorStore

# LangChain para agentes
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

# Hybrid search
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)
```

## Alternativas Consideradas

| Alternativa | Prós | Contras | Decisão |
|------------|------|---------|---------|
| LlamaIndex only | Excelente RAG | Agents limitados | Rejeitado |
| LangChain only | Agents excelentes | RAG genérico | Rejeitado |
| **Híbrido** | **Melhor dos dois** | **Complexidade** | **Aceito** |

## Referências

- LlamaIndex: https://docs.llamaindex.ai/
- LangChain: https://python.langchain.com/
- LangGraph: https://langchain-ai.github.io/langgraph/
