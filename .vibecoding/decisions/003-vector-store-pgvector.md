# ADR-003: pgvector como Vector Store

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa armazenar embeddings vetoriais para RAG. Opções:
- Qdrant (dedicado para vectores)
- pgvector (extensão PostgreSQL)
- Weaviate, Milvus, etc.

## Decisão

Usar **pgvector** como vector store principal, migrando do Qdrant.

## Justificativa

### Por que pgvector?

1. **Unificação**: Um banco para dados relacionais + vetoriais
2. **Simplicidade**: Um backup, um restore, uma conexão
3. **Consistência**: Transações ACID envolvendo vectores + dados
4. **Row-Level Security**: Multi-tenancy nativo
5. **Madureza**: PostgreSQL é battle-tested

### Por que não Qdrant?

| Critério | Qdrant | pgvector |
|----------|--------|----------|
| Performance pura | Melhor | Bom |
| Complexidade ops | 2 bancos | 1 banco |
| Backup | Separado | Unificado |
| Multi-tenancy | Manual | Row-Level Security |
| Consistency | Eventual | ACID |
| Deploy | Extra container | Integrado |

### Performance

Para o volume do ImobPro.ai (10k-100k embeddings por tenant), pgvector é suficiente:
- HNSW index: ~1ms para top-10
- IVFFlat index: ~5ms para top-10
- Qdrant seria melhor para >1M embeddings

## Implementação

```python
from sqlalchemy import create_engine
from pgvector.sqlalchemy import Vector

# Migration
op.add_column('chunks', Column('embedding', Vector(1024)))
op.create_index('ix_chunks_embedding', 'chunks', 'embedding',
                postgresql_using='hnsw',
                postgresql_with={'m': 16, 'ef_construction': 64})
```

## Alternativas Consideradas

| Alternativa | Prós | Contras | Decisão |
|------------|------|---------|---------|
| Qdrant | Performance | 2 bancos, ops extras | Rejeitado |
| Weaviate | Features | Complexo, caro | Rejeitado |
| Pinecone | Managed | Vendor lock-in | Rejeitado |
| **pgvector** | **Simples, unificado** | **Performance inferior** | **Aceito** |

## Referências

- pgvector: https://github.com/pgvector/pgvector
- HNSW: https://db.cs.cmu.edu/papers/2019/p1261-malkov.pdf
