from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Auth ──────────────────────────────────────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── User ──────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str = "agent"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Tenant ────────────────────────────────────────────────────────────────────
class TenantCreate(BaseModel):
    name: str
    slug: str
    plan: str = "starter"
    commercial_rules: str = ""


class TenantResponse(BaseModel):
    id: str
    name: str
    slug: str
    plan: str
    config: dict
    commercial_rules: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Agent ─────────────────────────────────────────────────────────────────────
class AgentCreate(BaseModel):
    name: str
    voice_id: str = "nova"
    llm_model: str = "gpt-4o"
    system_prompt: str = ""
    phone_number: str | None = None
    whatsapp_instance: str | None = None


class AgentUpdate(BaseModel):
    name: str | None = None
    voice_id: str | None = None
    llm_model: str | None = None
    system_prompt: str | None = None
    is_active: bool | None = None
    phone_number: str | None = None
    whatsapp_instance: str | None = None


class AgentResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    voice_id: str
    llm_model: str
    is_active: bool
    phone_number: str | None
    whatsapp_instance: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Contact ───────────────────────────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    whatsapp: str | None = None
    tags: list[str] = []
    assigned_to: str | None = None


class ContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    whatsapp: str | None = None
    tags: list[str] | None = None
    score: int | None = None
    status: str | None = None
    assigned_to: str | None = None


class ContactResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    phone: str | None
    email: str | None
    whatsapp: str | None
    tags: list
    score: int
    status: str
    assigned_to: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Property ──────────────────────────────────────────────────────────────────
class PropertyCreate(BaseModel):
    title: str
    description: str = ""
    price: int = 0
    address: str = ""
    bedrooms: int = 0
    bathrooms: int = 0
    area_m2: int = 0
    property_type: str = "apartment"
    features: list[str] = []
    images: list[str] = []


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    address: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    area_m2: int | None = None
    property_type: str | None = None
    status: str | None = None
    features: list[str] | None = None
    images: list[str] | None = None


class PropertyResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: str
    price: int
    address: str
    bedrooms: int
    bathrooms: int
    area_m2: int
    property_type: str
    status: str
    features: list
    images: list
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Conversation ──────────────────────────────────────────────────────────────
class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    content_type: str
    metadata: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    id: str
    agent_id: str
    contact_id: str
    channel: str
    status: str
    summary: str
    sentiment: str | None
    intent: str | None
    created_at: datetime
    messages: list[MessageResponse] = []

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    id: str
    contact_name: str
    channel: str
    status: str
    summary: str
    last_message: str
    last_message_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ── FollowUp ──────────────────────────────────────────────────────────────────
class FollowUpCreate(BaseModel):
    contact_id: str
    scheduled_at: datetime
    message: str
    channel: str = "whatsapp"


class FollowUpResponse(BaseModel):
    id: str
    contact_id: str
    scheduled_at: datetime
    message: str
    channel: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Webhook ───────────────────────────────────────────────────────────────────
class WhatsAppWebhook(BaseModel):
    event: str
    instance: str
    data: dict


class VoiceWebhook(BaseModel):
    CallSid: str
    CallStatus: str
    From: str
    To: str
    Direction: str


# ── Dashboard / Metrics ──────────────────────────────────────────────────────
class DashboardMetrics(BaseModel):
    total_contacts: int
    active_conversations: int
    total_properties: int
    contacts_won: int
    contacts_lost: int
    conversion_rate: float
    messages_today: int
    avg_response_time_seconds: float


class ConversationMetrics(BaseModel):
    total: int
    by_channel: dict[str, int]
    by_status: dict[str, int]
    avg_messages_per_conversation: float
