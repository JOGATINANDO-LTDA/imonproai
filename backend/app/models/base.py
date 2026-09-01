from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="starter")
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    commercial_rules: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    agents: Mapped[list["Agent"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    contacts: Mapped[list["Contact"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    properties: Mapped[list["Property"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="agent")  # admin, manager, agent
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="users")


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    voice_id: Mapped[str] = mapped_column(String(100), default="nova")
    llm_model: Mapped[str] = mapped_column(String(100), default="gpt-4o")
    system_prompt: Mapped[str] = mapped_column(Text, default="")
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    whatsapp_instance: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="agents")
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="agent", cascade="all, delete-orphan"
    )


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(
        String(50), default="new"
    )  # new, qualified, proposal, won, lost
    assigned_to: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="contacts")
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="contact", cascade="all, delete-orphan"
    )
    follow_ups: Mapped[list["FollowUp"]] = relationship(
        back_populates="contact", cascade="all, delete-orphan"
    )


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[int] = mapped_column(Integer, default=0)
    address: Mapped[str] = mapped_column(String(500), default="")
    bedrooms: Mapped[int] = mapped_column(Integer, default=0)
    bathrooms: Mapped[int] = mapped_column(Integer, default=0)
    area_m2: Mapped[int] = mapped_column(Integer, default=0)
    property_type: Mapped[str] = mapped_column(
        String(50), default="apartment"
    )  # house, apartment, land, commercial
    status: Mapped[str] = mapped_column(
        String(50), default="available"
    )  # available, sold, rented, reserved
    features: Mapped[list] = mapped_column(JSONB, default=list)
    images: Mapped[list] = mapped_column(JSONB, default=list)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="properties")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    agent_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("agents.id"), nullable=False
    )
    contact_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("contacts.id"), nullable=False
    )
    channel: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # whatsapp, sms, email, voice, webchat
    status: Mapped[str] = mapped_column(String(50), default="active")  # active, closed, archived
    summary: Mapped[str] = mapped_column(Text, default="")
    sentiment: Mapped[str | None] = mapped_column(String(20), nullable=True)
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    agent: Mapped["Agent"] = relationship(back_populates="conversations")
    contact: Mapped["Contact"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("conversations.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(50), default="text"
    )  # text, audio, image, document, pdf
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    contact_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("contacts.id"), nullable=False
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="whatsapp")
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, sent, failed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    contact: Mapped["Contact"] = relationship(back_populates="follow_ups")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
