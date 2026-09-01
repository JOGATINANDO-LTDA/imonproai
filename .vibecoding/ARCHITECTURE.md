# Arquitetura — ImobPro.ai

## Visão Geral

O ImobPro.ai segue uma arquitetura **multi-tenant** e **multi-provider**, projetada para:

- Isolamento de dados por imobiliária (tenant)
- Troca de provider de IA sem reescrever código
- Escala horizontal via containerização
- Observabilidade completa via Langfuse

## Camadas do Sistema

### 1. Frontend (Next.js 15)

**Responsabilidade**: Interface do usuário para gestão de leads, conversas e configurações.

- App Router para rotas server/client
- Server Components para dados sensíveis
- Streaming de respostas de IA via SSE
- shadcn/ui para componentes acessíveis

**Justificativa**: Next.js 15 oferece Server Components nativos, reduzindo bundle size e melhorando SEO. O App Router é o padrão oficial.

### 2. Backend (FastAPI)

**Responsabilidade**: API REST, autenticação, multi-tenancy, integrações.

- FastAPI para performance async
- SQLAlchemy 2.0 para ORM moderno
- JWT para autenticação
- Celery para tarefas assíncronas

**Justificativa**: FastAPI é o framework Python mais rápido para APIs, com suporte nativo a async/await e OpenAPI.

### 3. AI Engine (LangGraph)

**Responsabilidade**: Orquestração de IA, RAG, voz, evaluations.

- LangGraph para state machines complexas
- Provider Registry para multi-provider
- RAG engine com pgvector
- Pipeline de voz STT→LLM→TTS

**Justificativa**: LangGraph permite criar fluxos de IA com controle fino sobre estado, loops e fallbacks — essencial para um agente comercial.

### 4. Database (PostgreSQL + pgvector)

**Responsabilidade**: Dados relacionais + vectoriais.

- PostgreSQL 16 para dados principais
- pgvector para embeddings vetoriais
- Partitioning por tenant (ROW-LEVEL SECURITY)
- Backup automatizado

**Justificativa**: Unifica dados relacionais e vetoriais em um único banco, simplificando ops e mantendo consistência.

### 5. Cache/Fila (Redis + Celery)

**Responsabilidade**: Cache de sessões, fila de tarefas, rate limiting.

- Redis para cache distribuído
- Celery para tarefas assíncronas
- Celery Beat para agendamentos

**Justificativa**: Redis é o padrão para cache e filas em Python. Celery é maduro e bem documentado.

### 6. Observabilidade (Langfuse)

**Responsabilidade**: Tracing de chamadas de IA, métricas, custos.

- Langfuse self-hosted para dados Locais
- Tracing de cada passo do agente
- Dashboard de custos por provider
- Eval framework integrado

**Justificativa**: Langfuse é open-source, self-hosted, e específico para LLMs — oferece visibilidade que ferramentas genéricas de APM não dão.

## Fluxos Principais

### Fluxo 1: Conversa via WhatsApp

```
Lead envia WhatsApp
    → Webhook recebe mensagem
    → Busca sessão do lead no Redis
    → Chama AI Engine
        → RAG busca contexto relevante
        → LLM gera resposta
        → Valida com evaluator
    → Envia resposta via Evolution API
    → Registra no banco
    → Envia tracing para Langfuse
```

### Fluxo 2: Ligação Telefônica

```
Lead liga
    → Twilio recebe chamada
    → STT transcreve áudio (faster-whisper)
    → AI Engine processa
    → LLM gera resposta
    → TTS gera áudio (Edge TTS / Coqui)
    → Twilio reproduz áudio
```

### Fluxo 3: RAG Query

```
Pergunta do usuário
    → Hybrid search (vector + BM25)
    → Reranking (cross-encoder)
    → Top 4 chunks selecionados
    → LLM gera resposta grounded
    → Evaluator verifica faithfulness
    → Resposta retornada com citações
```

## Segurança

- **Multi-tenancy**: Row-Level Security no PostgreSQL
- **Autenticação**: JWT com refresh tokens
- **API Keys**: Gerenciadas via environment variables
- **LGPD**: Dados ficam no Brasil (quando local)
- **Audit Log**: Todas as ações são registradas

## Escala

| Componente | Estratégia |
|-----------|-----------|
| Backend | Horizontal via Docker replicas |
| Database | Read replicas + partitioning |
| Redis | Cluster mode |
| AI Engine | Workers independentes por provider |
| Frontend | CDN (Vercel / Cloudflare) |

## Referências

- [Decisões técnicas](decisions/)
- [Providers de IA](providers/)
- [Engine RAG](rag/)
- [Stack de voz](voice/)
