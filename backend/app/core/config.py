from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = "ImobPro.ai"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://imobpro:imobpro@localhost:5432/imobpro"
    DATABASE_URL_SYNC: str = "postgresql://imobpro:imobpro@localhost:5432/imobpro"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Auth
    JWT_SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION-super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OpenAI / LLM Provider
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MODEL_FAST: str = "gpt-4o-mini"

    # LMStudio
    LMSTUDIO_URL: str = "http://host.docker.internal:1234"

    # Opencode ZEN (gratuito)
    OPencode_ZEN_API_KEY: str = ""

    # Groq
    GROQ_API_KEY: str = ""

    # OpenRouter
    OPENROUTER_API_KEY: str = ""

    # Kilo Gateway
    KILO_API_KEY: str = ""

    # Opencode Go ($10/mês)
    OPENCODE_GO_API_KEY: str = ""

    # Model Manager
    MODEL_TTL_SECONDS: int = 300
    MODEL_FALLBACK_PROVIDER: str = "opencode-zen"
    MODEL_DEFAULT: str = "qwen3.5-9b-deepseek-v4-flash"

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "imobpro-ai"

    # Twilio (Voz/Telefone)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    TWILIO_WEBHOOK_URL: str = ""

    # WhatsApp (Evolution API)
    EVOLUTION_API_URL: str = ""
    EVOLUTION_API_KEY: str = ""

    # Email (SMTP)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # S3 / Storage
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "imobpro-ai-docs"

    # Qdrant (Vector DB)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3010", "http://localhost:8000"]

    # Agent defaults
    AGENT_MAX_ITERATIONS: int = 15
    AGENT_TEMPERATURE: float = 0.7
    AGENT_SYSTEM_PROMPT_TEMPLATE: str = """Você é um agente comercial de IA especializado em imobiliárias.

IDENTIDADE:
- Seu nome é {agent_name}
- Você trabalha para a imobiliária {tenant_name}
- Você é educado, profissional e focado em converter leads em visitas/agendamentos

CAPACIDADES:
- Responder mensagens de texto (WhatsApp, SMS, E-mail)
- Processar áudio (transcrição) e responder por áudio
- Analisar imagens de imóveis enviadas pelos leads
- Interpretar documentos e PDFs
- Fazer follow-ups automáticos
- Agendar visitas e compromissos
- Consultar informações de imóveis do portfólio

REGRAS COMERCIAIS (personalizadas por cliente):
{commercial_rules}

MEMÓRIA DO CLIENTE:
{client_context}

DIRETRIZES:
1. Sempre cumprimente o lead pelo nome quando disponível
2. Seja conciso em respostas de WhatsApp (máx 3 frases)
3. Nunca invente informações sobre imóveis - apenas use dados do portfólio
4. Se o lead demonstrar interesse, ofereça agendamento de visita
5. Em caso de objeção sobre preço, destaque valor e benefícios
6. Faça follow-up em 24h se não houver resposta
7. Encaminhe para humano quando: reclamação formal, negociação de desconto >10%, ou pedido explicito"""


def get_settings() -> Settings:
    return Settings()
