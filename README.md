# ImobPro.ai — Agente Comercial de IA para Imobiliárias

> Plataforma de IA conversacional para automação de vendas imobiliárias.
> Multi-tenant, multi-provider, com RAG, voz e CRM integrado.

## Visão Geral

O ImobPro.ai é um agente comercial inteligente que automatiza:
- **Atendimento 24/7** via WhatsApp, telefone e web
- **Qualificação de leads** com perguntas estratégicas
- **Agendamento de visitas** integrado ao Google Calendar
- **Follow-up automático** personalizado por lead
- **CRM completo** com pipeline de vendas

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                    │
│  Dashboard │ CRM │ Conversas │ Configurações │ Login     │
└─────────────────────────┬───────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────┐
│                   BACKEND (FastAPI)                       │
│  Auth │ Multi-tenant │ CRUD │ Webhooks │ Celery Tasks    │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                  AI ENGINE (LangGraph)                    │
│  Provider Registry │ RAG Engine │ TTS/STT │ Evals        │
└──────┬──────────────┬──────────────┬────────────────────┘
       │              │              │
  ┌────▼────┐   ┌─────▼─────┐  ┌─────▼─────┐
  │LMStudio │   │  Opencode  │  │  Groq /   │
  │ (Local) │   │ ZEN / GO   │  │ Together  │
  └─────────┘   └───────────┘  └───────────┘
```

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Frontend | Next.js 15, Tailwind CSS, shadcn/ui |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0 |
| AI Engine | LangGraph, LangChain, LlamaIndex |
| Database | PostgreSQL 16 + pgvector |
| Cache/Fila | Redis 7, Celery 5 |
| Observabilidade | Langfuse (self-hosted) |
| Containerização | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deploy | Render / Docker |

## Providers de IA

| Provider | Tipo | Custo | Uso |
|----------|------|-------|-----|
| LMStudio | Local | $0 | Desenvolvimento, MVP |
| Opencode ZEN | Cloud Free | $0 | Modelos gratuitos |
| Opencode GO | Cloud Pago | $10/mês | Produção |
| Groq | Cloud Free | $0 | Inferência rápida |
| Together AI | Cloud Free | $0 | Modelos open-source |
| OpenAI | BYOK | Variável | Clientes premium |

## Setup Rápido

```bash
# 1. Clone
git clone https://github.com/JOGATINANDO-LTDA/imonproai.git
cd imonproai

# 2. Configure
cp .env.example .env
# Edite .env com suas credenciais

# 3. Execute
docker compose up -d

# 4. Acesse
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

## Estrutura do Projeto

```
imobpro-ai/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── agent/       # Engine de IA (LangGraph)
│   │   ├── api/         # Endpoints REST
│   │   ├── core/        # Config, auth, database
│   │   ├── integrations/# WhatsApp, Voice, Email
│   │   ├── models/      # SQLAlchemy models
│   │   └── tasks/       # Celery tasks
│   └── tests/
├── frontend/             # Next.js 15
│   └── src/
│       ├── app/         # App Router pages
│       ├── components/  # React components
│       └── lib/         # API client, utils
├── .vibecoding/          # Sistema de decisão agentico
├── .github/              # CI/CD workflows
├── docker-compose.yml
└── render.yaml
```

## Documentação

- **Arquitetura**: `.vibecoding/ARCHITECTURE.md`
- **Decisões técnicas**: `.vibecoding/decisions/`
- **Providers de IA**: `.vibecoding/providers/`
- **Engine RAG**: `.vibecoding/rag/`
- **Stack de voz**: `.vibecoding/voice/`
- **Guias**: `.vibecoding/guides/`

## Licença

Proprietário — JOGATINANDO LTDA
