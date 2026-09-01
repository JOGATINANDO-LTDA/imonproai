# Guia de Setup Local — ImobPro.ai

## Pré-requisitos

- Python 3.11+
- Node.js 20+
- Docker Desktop
- Git
- LMStudio (para modelos locais)

## Passo 1: Clone

```bash
git clone https://github.com/JOGATINANDO-LTDA/imonproai.git
cd imonproai
```

## Passo 2: Configure

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/imobpro

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=sua-chave-secreta
JWT_ALGORITHM=HS256

# LMStudio
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio

# Opencode (opcional)
OPENCODE_ZEN_API_KEY=
OPENCODE_GO_API_KEY=

# WhatsApp (Evolution API)
WHATSAPP_API_URL=http://localhost:8080
WHATSAPP_API_KEY=

# Twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## Passo 3: Execute

```bash
docker compose up -d
```

## Passo 4: Acesse

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## Passo 5: Popule o Banco

```bash
docker compose exec backend python scripts/seed_db.py
```

## Credenciais Padrão

| Email | Senha | Perfil |
|-------|-------|--------|
| admin@imobpro.ai | admin123 | admin |
| agente@imobpro.ai | agente123 | agent |

## Desenvolvimento

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Erro de conexão com LMStudio

1. Abra o LMStudio
2. Carregue um modelo
3. Inicie o servidor local (port 1234)

### Erro de banco de dados

```bash
docker compose down -v
docker compose up -d
docker compose exec backend python scripts/seed_db.py
```

## Referências

- [Docker Guide](docker-guide.md)
- [Git Flow Guide](git-flow-guide.md)
