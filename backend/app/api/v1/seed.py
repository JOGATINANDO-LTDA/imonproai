import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import hash_password
from app.models.base import (
    Agent,
    Contact,
    Conversation,
    FollowUp,
    Message,
    Property,
    Tenant,
    User,
)

settings = get_settings()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/seed", tags=["Seed"])

TENANT_ID = "00000000-0000-0000-0000-000000000000"


async def _tenant_exists(db: AsyncSession) -> bool:
    result = await db.execute(select(Tenant).where(Tenant.id == TENANT_ID))
    return result.scalar_one_or_none() is not None


@router.post("")
async def seed_demo_data(db: AsyncSession = Depends(get_db)):
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Seed só disponível em modo DEBUG")

    if await _tenant_exists(db):
        return {"message": "Dados demo já existem", "skipped": True}

    # ── Tenant ────────────────────────────────────────────────────────────
    tenant = Tenant(
        id=TENANT_ID,
        name="Imobiliária Modelo",
        slug="imob-modelo",
        plan="professional",
        commercial_rules=(
            "Não oferecer descontos superiores a 5%. "
            "Sempre agendar visitas para período da manhã ou tarde. "
            "Priorizar imóveis com vista e aceitar negociação em até 3x parcelas."
        ),
    )
    db.add(tenant)

    # ── User ──────────────────────────────────────────────────────────────
    user = User(
        tenant_id=TENANT_ID,
        email="admin@imobpro.ai",
        hashed_password=hash_password("admin123"),
        full_name="Carlos Mendes",
        role="admin",
    )
    db.add(user)

    # ── Agents ────────────────────────────────────────────────────────────
    agent1 = Agent(
        tenant_id=TENANT_ID,
        name="Assistente Virtual",
        voice_id="nova",
        llm_model="qwen3.5-9b-deepseek-v4-flash",
        system_prompt=(
            "Você é um assistente virtual da Imobiliária Modelo. "
            "Ajude clientes a encontrar imóveis ideais. "
            "Seja educado, profissional e objetivo."
        ),
        phone_number="(11) 99999-0001",
        whatsapp_instance="imob-modelo-main",
    )
    agent2 = Agent(
        tenant_id=TENANT_ID,
        name="Consultor Especializado",
        voice_id="vera",
        llm_model="qwen3.5-9b-deepseek-v4-flash",
        system_prompt=(
            "Você é um consultor imobiliário especializado em imóveis de alto padrão. "
            "Tenha conhecimento detalhado sobre bairros, valores e condições de pagamento."
        ),
        phone_number="(11) 99999-0002",
        whatsapp_instance="imob-modelo-crm",
    )
    db.add_all([agent1, agent2])
    await db.flush()

    # ── Contacts ──────────────────────────────────────────────────────────
    contacts_data = [
        ("Maria Silva", "(11) 98765-4321", "maria.silva@email.com", "(11) 98765-4321", "won", 95),
        ("João Santos", "(11) 97654-3210", "joao.santos@email.com", "(11) 97654-3210", "qualified", 72),
        ("Ana Oliveira", "(21) 99876-5432", "ana.oliveira@email.com", "(21) 99876-5432", "proposal", 85),
        ("Pedro Costa", "(31) 98123-4567", "pedro.costa@email.com", "(31) 98123-4567", "new", 45),
        ("Luciana Ferreira", "(41) 99234-5678", "luciana.f@email.com", "(41) 99234-5678", "won", 88),
        ("Roberto Almeida", "(11) 98456-7890", "roberto.a@email.com", None, "lost", 30),
        ("Fernanda Lima", "(21) 99765-4321", "fernanda.lima@email.com", "(21) 99765-4321", "qualified", 67),
        ("Marcos Souza", "(51) 99876-1234", "marcos.souza@email.com", "(51) 99876-1234", "proposal", 78),
    ]
    contacts = []
    for name, phone, email, whatsapp, status, score in contacts_data:
        c = Contact(
            tenant_id=TENANT_ID,
            name=name,
            phone=phone,
            email=email,
            whatsapp=whatsapp,
            status=status,
            score=score,
            tags=[status],
        )
        db.add(c)
        contacts.append(c)
    await db.flush()

    # ── Properties ────────────────────────────────────────────────────────
    properties_data = [
        {
            "title": "Apartamento Jardins 3 quartos",
            "description": "Apartamento amplo nos Jardins com vista para o parque. Próximo ao metrô e comércio.",
            "price": 850000,
            "address": "Rua dos Jardins, 450 - Jardins, São Paulo/SP",
            "bedrooms": 3,
            "bathrooms": 2,
            "area_m2": 120,
            "property_type": "apartment",
            "status": "available",
            "features": ["Varanda", "Ar condicionado", "Portaria 24h", "Estacionamento"],
        },
        {
            "title": "Cobertura Vila Mariana",
            "description": "Cobertura de alto padrão com terraço privativo e vista panorâmica da cidade.",
            "price": 1500000,
            "address": "Rua Harmonia, 120 - Vila Mariana, São Paulo/SP",
            "bedrooms": 4,
            "bathrooms": 3,
            "area_m2": 200,
            "property_type": "apartment",
            "status": "available",
            "features": ["Terraço", "Piscina privativa", "Churrasqueira", "Smart home"],
        },
        {
            "title": "Casa Alphaville 4 quartos",
            "description": "Casa moderna no Alphaville com jardim amplo e área de lazer completa.",
            "price": 2200000,
            "address": "Alameda dos Anjos, 78 - Alphaville, Barueri/SP",
            "bedrooms": 4,
            "bathrooms": 4,
            "area_m2": 350,
            "property_type": "house",
            "status": "available",
            "features": ["Piscina", "Churrasqueira", "Jardim", "Garagem 3 carros"],
        },
        {
            "title": "Studio Paulista",
            "description": "Studio compacto e moderno na Paulista. Ideal para profissionais.",
            "price": 420000,
            "address": "Rua Augusta, 1500 - Consolação, São Paulo/SP",
            "bedrooms": 1,
            "bathrooms": 1,
            "area_m2": 45,
            "property_type": "apartment",
            "status": "available",
            "features": ["Mobiliado", "Academia", "Coworking", "Rooftop"],
        },
        {
            "title": "Sala Comercial Faria Lima",
            "description": "Sala comercial premium na Faria Lima com vista privilegiada.",
            "price": 980000,
            "address": "Av. Faria Lima, 3000 - Itaim Bibi, São Paulo/SP",
            "bedrooms": 0,
            "bathrooms": 2,
            "area_m2": 80,
            "property_type": "commercial",
            "status": "available",
            "features": ["Ar condicionado central", "Recepcionista", "Segurança 24h"],
        },
        {
            "title": "Apartamento Moema 2 quartos",
            "description": "Apartamento aconchegante na Moema, próximo ao Parque Ibirapuera.",
            "price": 650000,
            "address": "Rua Canário, 300 - Moema, São Paulo/SP",
            "bedrooms": 2,
            "bathrooms": 2,
            "area_m2": 75,
            "property_type": "apartment",
            "status": "reserved",
            "features": ["Varanda", "Área de serviço", "Portaria", "Playground"],
        },
    ]
    properties = []
    for pdata in properties_data:
        p = Property(tenant_id=TENANT_ID, **pdata)
        db.add(p)
        properties.append(p)
    await db.flush()

    # ── Conversations & Messages ──────────────────────────────────────────
    now = datetime.utcnow()

    # Conversation 1: Maria Silva - WhatsApp
    conv1 = Conversation(
        agent_id=agent1.id,
        contact_id=contacts[0].id,
        channel="whatsapp",
        status="active",
        summary="Interesse em apartamento 3 quartos nos Jardins",
        sentiment="positive",
        intent="buy",
    )
    db.add(conv1)
    await db.flush()

    msgs1 = [
        (now - timedelta(minutes=45), "user", "Olá! Vi um apartamento no site e tenho interesse."),
        (now - timedelta(minutes=44), "assistant", "Olá Maria! Ficamos felizes com seu interesse! Posso te ajudar a encontrar o imóvel perfeito. Qual sua faixa de preço e região preferida?"),
        (now - timedelta(minutes=42), "user", "Até R$ 900.000, perto do metrô na região dos Jardins."),
        (now - timedelta(minutes=41), "assistant", "Perfeito! Temos um apartamento incrível nos Jardins com 3 quartos, 120m², por R$ 850.000. Possui varanda, ar condicionado e portaria 24h. Posso agendar uma visita para você?"),
    ]
    for ts, role, content in msgs1:
        db.add(Message(conversation_id=conv1.id, role=role, content=content, created_at=ts))

    # Conversation 2: João Santos - Voice
    conv2 = Conversation(
        agent_id=agent2.id,
        contact_id=contacts[1].id,
        channel="voice",
        status="active",
        summary="Consulta sobre cobertura na Vila Mariana",
        sentiment="neutral",
        intent="inquiry",
    )
    db.add(conv2)
    await db.flush()

    msgs2 = [
        (now - timedelta(hours=2), "user", "Bom dia, gostaria de informações sobre coberturas na Vila Mariana."),
        (now - timedelta(hours=2), "assistant", "Bom dia João! Temos uma cobertura exclusiva na Vila Mariana com 4 quartos, terraço privativo e vista panorâmica. O valor é R$ 1.500.000. Posso enviar mais detalhes por WhatsApp?"),
        (now - timedelta(hours=1, minutes=55), "user", "Sim, pode enviar. Meu WhatsApp é (11) 97654-3210."),
    ]
    for ts, role, content in msgs2:
        db.add(Message(conversation_id=conv2.id, role=role, content=content, created_at=ts))

    # Conversation 3: Ana Oliveira - Email
    conv3 = Conversation(
        agent_id=agent1.id,
        contact_id=contacts[2].id,
        channel="email",
        status="active",
        summary="Proposta para casa em Alphaville",
        sentiment="positive",
        intent="buy",
    )
    db.add(conv3)
    await db.flush()

    msgs3 = [
        (now - timedelta(hours=5), "user", "Prezados, tenho interesse na casa em Alphaville. Podemos negociar o valor?"),
        (now - timedelta(hours=4), "assistant", "Olá Ana! A casa em Alphaville está disponível por R$ 2.200.000. Podemos oferecer condições especiais de pagamento: entrada + 24 parcelas. Gostaria de agendar uma visita para conhecer o imóvel?"),
    ]
    for ts, role, content in msgs3:
        db.add(Message(conversation_id=conv3.id, role=role, content=content, created_at=ts))

    # ── Follow-ups ────────────────────────────────────────────────────────
    followups = [
        FollowUp(
            contact_id=contacts[1].id,
            tenant_id=TENANT_ID,
            scheduled_at=now + timedelta(days=1, hours=10),
            message="Olá João! Vim verificar seu interesse na cobertura Vila Mariana. Podemos agendar uma visita?",
            channel="whatsapp",
            status="pending",
        ),
        FollowUp(
            contact_id=contacts[3].id,
            tenant_id=TENANT_ID,
            scheduled_at=now + timedelta(days=2, hours=14),
            message="Olá Pedro! Temos imóveis que podem combinar com seu perfil. Posso te mostrar as opções?",
            channel="whatsapp",
            status="pending",
        ),
    ]
    db.add_all(followups)

    await db.commit()

    logger.info("Seed demo criado com sucesso!")

    return {
        "message": "Dados demo criados com sucesso",
        "skipped": False,
        "data": {
            "tenant": "Imobiliária Modelo",
            "user": "admin@imobpro.ai",
            "contacts": len(contacts_data),
            "properties": len(properties_data),
            "agents": 2,
            "conversations": 3,
        },
    }
