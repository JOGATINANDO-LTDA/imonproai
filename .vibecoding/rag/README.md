# Engine RAG — ImobPro.ai

## Visão Geral

O RAG (Retrieval-Augmented Generation) do ImobPro.ai permite que o agente comercial acesse informações de imóveis, documentos e contextos para gerar respostas precisas e grounded.

## Arquitetura

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  INGESTION   │    │   INDEXING   │    │  RETRIEVAL   │
│              │    │              │    │              │
│ PDF → text   │───▶│ Chunking     │───▶│ Hybrid Search│
│ IMG → OCR    │    │ Embedding    │    │ Vector+BM25  │
│ DOCX → text  │    │ pgvector     │    │              │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
┌──────────────┐    ┌──────────────┐    ┌──────▼───────┐
│  GENERATION  │    │  EVALUATION  │    │  RERANKING   │
│              │◀───│              │◀───│              │
│ LLM + context│    │ Faithfulness │    │ Cross-encoder│
│ + citations  │    │ Relevancy    │    │ BAAI/bge     │
│              │    │ Recall       │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Componentes

### 1. Ingestion

| Fonte | Ferramenta | Output |
|-------|-----------|--------|
| PDF | PyMuPDF | Texto |
| Imagem | Tesseract | Texto (OCR) |
| DOCX | python-docx | Texto |
| Web | BeautifulSoup | Texto |

### 2. Chunking

| Estratégia | Quando | Chunk Size | Overlap |
|-----------|--------|-----------|---------|
| Fixed | Textos simples | 512 | 50 |
| Recursive | Documentos longos | 1024 | 100 |
| Semantic | Temas distintos | Variável | 0 |

### 3. Embeddings

| Provider | Modelo | Dimensão | Custo |
|----------|--------|----------|-------|
| Local | all-MiniLM-L6-v2 | 384 | $0 |
| Local | bge-large-pt-v1.5 | 1024 | $0 |
| OpenAI | text-embedding-3-small | 1536 | $0.02/1M |

### 4. Vector Store

**pgvector** — Unificado com PostgreSQL

```python
from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    embedding = Column(Vector(1024))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
```

### 5. Hybrid Search

```python
# Combinação de busca vetorial + BM25
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]  # Configurável por tenant
)
```

### 6. Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-base")
# Pega top 10 do retrieval, retorna top 4 após reranking
```

### 7. Evals

| Métrica | Target | Framework |
|---------|--------|-----------|
| Faithfulness | > 0.8 | Ragas |
| Relevancy | > 0.7 | Ragas |
| Context Recall | > 0.75 | Ragas |
| Context Precision | > 0.7 | Ragas |

## Config por Tenant

```yaml
embedding:
  provider: "local"
  model: "bge-large-pt-v1.5"

chunking:
  strategy: "recursive"
  chunk_size: 1024
  chunk_overlap: 100

retrieval:
  mode: "hybrid"
  vector_weight: 0.6
  bm25_weight: 0.4
  top_k: 10
  rerank_top_n: 4

generation:
  provider: "lmstudio"
  model: "qwen3.5-9b-deepseek-v4-flash"
  temperature: 0.7
```

## Referências

- [ADR-002: Engine RAG](../decisions/002-rag-engine-choice.md)
- [ADR-003: pgvector](../decisions/003-vector-store-pgvector.md)
- LlamaIndex: https://docs.llamaindex.ai/
