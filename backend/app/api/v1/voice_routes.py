import logging
from typing import Any

from fastapi import APIRouter, Form, Request, Response
from sqlalchemy import select

from app.agent.engine import ImobProAgent
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.integrations.voice import VoiceService
from app.models.base import Agent, Contact, Conversation, Message, Tenant

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/voice", tags=["Voice"])

voice_service = VoiceService()


@router.post("/inbound")
async def voice_inbound(From: str = Form(...), To: str = Form(...), CallSid: str = Form(...)):
    phone = From.replace("+", "")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Agent).where(Agent.phone_number == To))
        agent = result.scalar_one_or_none()
        if not agent:
            twiml = voice_service.create_callback_twiml("Desculpe, não consegui atender sua chamada.")
            return Response(content=twiml, media_type="application/xml")

        contact_result = await db.execute(
            select(Contact).where(Contact.phone == phone, Contact.tenant_id == agent.tenant_id)
        )
        contact = contact_result.scalar_one_or_none()
        if not contact:
            contact = Contact(
                tenant_id=agent.tenant_id,
                name=phone,
                phone=phone,
                status="new",
            )
            db.add(contact)
            await db.flush()

        conversation = Conversation(
            agent_id=agent.id,
            contact_id=contact.id,
            channel="voice",
            status="active",
        )
        db.add(conversation)
        await db.flush()
        await db.commit()

    twiml = voice_service.create_inbound_twiml()
    return Response(content=twiml, media_type="application/xml")


@router.post("/speech-result")
async def voice_speech_result(
    SpeechResult: str = Form(...),
    CallSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
):
    phone = From.replace("+", "")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Agent).where(Agent.phone_number == To))
        agent = result.scalar_one_or_none()
        if not agent:
            twiml = voice_service.create_callback_twiml("Desculpe, ocorreu um erro.")
            return Response(content=twiml, media_type="application/xml")

        contact_result = await db.execute(
            select(Contact).where(Contact.phone == phone, Contact.tenant_id == agent.tenant_id)
        )
        contact = contact_result.scalar_one_or_none()

        conv_result = await db.execute(
            select(Conversation).where(
                Conversation.agent_id == agent.id,
                Conversation.contact_id == contact.id if contact else False,
                Conversation.channel == "voice",
                Conversation.status == "active",
            )
        )
        conversation = conv_result.scalar_one_or_none()
        if not conversation:
            twiml = voice_service.create_callback_twiml("Desculpe, não encontrei sua conversa.")
            return Response(content=twiml, media_type="application/xml")

        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=SpeechResult,
            content_type="text",
        )
        db.add(user_msg)

        tenant_result = await db.execute(select(Tenant).where(Tenant.id == agent.tenant_id))
        tenant = tenant_result.scalar_one_or_none()

        ai_agent = ImobProAgent(
            tenant_name=tenant.name if tenant else "Imobiliária",
            agent_name=agent.name,
            commercial_rules=tenant.commercial_rules if tenant else "",
            llm_model=agent.llm_model,
        )

        hist_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(20)
        )
        history = [
            {"role": m.role, "content": m.content}
            for m in reversed(hist_result.scalars().all())
        ]

        ai_response = await ai_agent.process_message(
            user_message=SpeechResult,
            channel="voice",
            history=history,
            context={
                "tenant_id": agent.tenant_id,
                "contact_id": contact.id if contact else "",
                "phone": phone,
            },
        )

        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response,
            content_type="text",
        )
        db.add(assistant_msg)
        await db.commit()

    twiml = voice_service.create_speech_response(ai_response, continue_listening=True)
    return Response(content=twiml, media_type="application/xml")


@router.post("/outbound")
async def voice_outbound(to: str, agent_id: str, message: str = ""):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if not agent:
            return {"error": "Agente não encontrado"}

        url = f"{settings.TWILIO_WEBHOOK_URL}/api/v1/voice/inbound"
        call_result = voice_service.make_call(to=to, url=url)
        return {"status": "calling", "call_sid": call_result["call_sid"]}


@router.post("/status")
async def voice_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    CallDuration: str = Form(None),
):
    logger.info(f"Status da chamada {CallSid}: {CallStatus} (duração: {CallDuration}s)")
    return Response(status_code=200)
