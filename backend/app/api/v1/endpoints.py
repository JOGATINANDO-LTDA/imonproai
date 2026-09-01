from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.base import Agent, Contact, Conversation, Property, Tenant, User
from app.schemas.schemas import (
    AgentCreate,
    AgentResponse,
    AgentUpdate,
    ContactCreate,
    ContactResponse,
    ContactUpdate,
    ConversationListResponse,
    ConversationResponse,
    DashboardMetrics,
    FollowUpCreate,
    FollowUpResponse,
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
    TenantCreate,
    TenantResponse,
    UserResponse,
)

router = APIRouter(prefix="/v1", tags=["API v1"])


# ── Tenants ───────────────────────────────────────────────────────────────────
@router.post("/tenants", response_model=TenantResponse, status_code=201)
async def create_tenant(body: TenantCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    tenant = Tenant(**body.model_dump())
    db.add(tenant)
    await db.flush()
    await db.refresh(tenant)
    return tenant


@router.get("/tenants", response_model=list[TenantResponse])
async def list_tenants(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "admin":
        result = await db.execute(select(Tenant))
    else:
        result = await db.execute(select(Tenant).where(Tenant.id == user.tenant_id))
    return result.scalars().all()


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and user.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    return tenant


# ── Users ─────────────────────────────────────────────────────────────────────
@router.get("/users", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "admin":
        result = await db.execute(select(User))
    elif user.role == "manager":
        result = await db.execute(select(User).where(User.tenant_id == user.tenant_id))
    else:
        result = await db.execute(select(User).where(User.id == user.id))
    return result.scalars().all()


# ── Agents ────────────────────────────────────────────────────────────────────
@router.post("/agents", response_model=AgentResponse, status_code=201)
async def create_agent(body: AgentCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    agent = Agent(tenant_id=user.tenant_id, **body.model_dump())
    db.add(agent)
    await db.flush()
    await db.refresh(agent)
    return agent


@router.get("/agents", response_model=list[AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Agent).where(Agent.tenant_id == user.tenant_id))
    return result.scalars().all()


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Agent).where(Agent.id == agent_id, Agent.tenant_id == user.tenant_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    return agent


@router.patch("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str, body: AgentUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Agent).where(Agent.id == agent_id, Agent.tenant_id == user.tenant_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)
    await db.flush()
    await db.refresh(agent)
    return agent


# ── Contacts ──────────────────────────────────────────────────────────────────
@router.post("/contacts", response_model=ContactResponse, status_code=201)
async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    contact = Contact(tenant_id=user.tenant_id, **body.model_dump())
    db.add(contact)
    await db.flush()
    await db.refresh(contact)
    return contact


@router.get("/contacts", response_model=list[ContactResponse])
async def list_contacts(
    status_filter: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Contact).where(Contact.tenant_id == user.tenant_id)
    if status_filter:
        query = query.where(Contact.status == status_filter)
    query = query.order_by(Contact.updated_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Contact).where(Contact.id == contact_id, Contact.tenant_id == user.tenant_id)
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contact


@router.patch("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str, body: ContactUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Contact).where(Contact.id == contact_id, Contact.tenant_id == user.tenant_id)
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    await db.flush()
    await db.refresh(contact)
    return contact


# ── Properties ────────────────────────────────────────────────────────────────
@router.post("/properties", response_model=PropertyResponse, status_code=201)
async def create_property(body: PropertyCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    prop = Property(tenant_id=user.tenant_id, **body.model_dump())
    db.add(prop)
    await db.flush()
    await db.refresh(prop)
    return prop


@router.get("/properties", response_model=list[PropertyResponse])
async def list_properties(
    property_type: str | None = None,
    status_filter: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Property).where(Property.tenant_id == user.tenant_id)
    if property_type:
        query = query.where(Property.property_type == property_type)
    if status_filter:
        query = query.where(Property.status == status_filter)
    if min_price:
        query = query.where(Property.price >= min_price)
    if max_price:
        query = query.where(Property.price <= max_price)
    query = query.order_by(Property.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Property).where(Property.id == property_id, Property.tenant_id == user.tenant_id)
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return prop


@router.patch("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str, body: PropertyUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Property).where(Property.id == property_id, Property.tenant_id == user.tenant_id)
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    await db.flush()
    await db.refresh(prop)
    return prop


# ── Conversations ─────────────────────────────────────────────────────────────
@router.get("/conversations", response_model=list[ConversationListResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Conversation)
        .join(Agent, Agent.id == Conversation.agent_id)
        .where(Agent.tenant_id == user.tenant_id)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conv


# ── Dashboard ─────────────────────────────────────────────────────────────────
@router.get("/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    tenant_id = user.tenant_id

    total_contacts = (
        await db.execute(select(func.count(Contact.id)).where(Contact.tenant_id == tenant_id))
    ).scalar() or 0

    total_properties = (
        await db.execute(select(func.count(Property.id)).where(Property.tenant_id == tenant_id))
    ).scalar() or 0

    contacts_won = (
        await db.execute(
            select(func.count(Contact.id)).where(Contact.tenant_id == tenant_id, Contact.status == "won")
        )
    ).scalar() or 0

    contacts_lost = (
        await db.execute(
            select(func.count(Contact.id)).where(Contact.tenant_id == tenant_id, Contact.status == "lost")
        )
    ).scalar() or 0

    conversion_rate = (contacts_won / total_contacts * 100) if total_contacts > 0 else 0.0

    return DashboardMetrics(
        total_contacts=total_contacts,
        active_conversations=0,
        total_properties=total_properties,
        contacts_won=contacts_won,
        contacts_lost=contacts_lost,
        conversion_rate=round(conversion_rate, 2),
        messages_today=0,
        avg_response_time_seconds=0.0,
    )
