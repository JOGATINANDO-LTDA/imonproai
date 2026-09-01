# ADR-009: Docker por Ambiente

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O projeto precisa de ambientes isolados:
- **Desenvolvimento**: Local, dados fictícios
- **Staging**: Homologação, dados de teste
- **Produção**: Dados reais, alta disponibilidade

## Decisão

Usar **Docker Compose** para dev/staging e **Render** para produção.

### docker-compose.yml (Dev)

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [postgres, redis]

  celery-worker:
    build: ./backend
    command: celery -A app.tasks worker
    depends_on: [redis, postgres]

  celery-beat:
    build: ./backend
    command: celery -A app.tasks beat
    depends_on: [redis]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
```

### render.yaml (Produção)

```yaml
services:
  - type: web
    name: imobpro-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app

  - type: web
    name: imobpro-frontend
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm start

  - type: postgres
    name: imobpro-db
    plan: starter
```

## Justificativa

### Por que Docker Compose para dev?

- **Simples**: Um comando sobe tudo
- **Isolado**: Não conflita com其他 projetos
- **Reprodutível**: Mesmo ambiente para toda equipe
- **Fácil de limpar**: `docker compose down -v`

### Por que Render para produção?

- **Gratuito tier**: Para MVP
- **Managed**: Sem ops de infra
- **Auto-deploy**: Deploy automático do GitHub
- **PostgreSQL managed**: Sem backup manual

## Ambientes

| Ambiente | Infra | Dados | URL |
|----------|-------|-------|-----|
| Dev | Docker Compose | Fictícios | localhost |
| Staging | Docker Compose | Teste | staging.imobpro.ai |
| Production | Render | Reais | imobpro.ai |

## Referências

- Docker Compose: https://docs.docker.com/compose/
- Render: https://render.com/
- pgvector: https://github.com/pgvector/pgvector
