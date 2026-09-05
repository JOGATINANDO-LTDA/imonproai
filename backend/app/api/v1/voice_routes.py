import base64
import logging

from fastapi import APIRouter, Form, Response
from pydantic import BaseModel
from sqlalchemy import select

from app.agent.engine import ImobProAgent
from app.agent.voice.tts import TTSEngine
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.integrations.voice import VoiceService
from app.models.base import Agent, Contact, Conversation, Message, Tenant

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/voice", tags=["Voice"])

voice_service = VoiceService()
tts_engine = TTSEngine(provider="edge", voice_id="pt-BR-FranciscaNeural")


class SimulateRequest(BaseModel):
    message: str
    agent_id: str | None = None
    conversation_id: str | None = None


@router.post("/simulate")
async def voice_simulate(req: SimulateRequest):
    """Simula uma ligação de voz localmente (sem Twilio)."""
    try:
        async with AsyncSessionLocal() as db:
            if req.agent_id:
                result = await db.execute(select(Agent).where(Agent.id == req.agent_id))
            else:
                result = await db.execute(select(Agent).limit(1))
            agent = result.scalar_one_or_none()
            if not agent:
                return {"error": "Nenhum agente encontrado. Crie um agente primeiro."}

            tenant_result = await db.execute(select(Tenant).where(Tenant.id == agent.tenant_id))
            tenant = tenant_result.scalar_one_or_none()

            if req.conversation_id:
                conv_result = await db.execute(
                    select(Conversation).where(Conversation.id == req.conversation_id)
                )
                conversation = conv_result.scalar_one_or_none()
            else:
                contact = Contact(
                    tenant_id=agent.tenant_id,
                    name="Teste Local",
                    phone="000000000",
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

            user_msg = Message(
                conversation_id=conversation.id,
                role="user",
                content=req.message,
                content_type="text",
            )
            db.add(user_msg)

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
                .limit(20),
            )
            history = [
                {"role": m.role, "content": m.content} for m in reversed(hist_result.scalars().all())
            ]

            ai_response = await ai_agent.process_message(
                user_message=req.message,
                channel="voice",
                history=history,
                context={
                    "tenant_id": agent.tenant_id,
                    "contact_id": contact.id,
                    "phone": "000000000",
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

        audio_bytes = await tts_engine.synthesize(ai_response)
        audio_b64 = base64.b64encode(audio_bytes).decode() if audio_bytes else ""

        return {
            "response": ai_response,
            "audio": audio_b64,
            "conversation_id": str(conversation.id),
        }
    except Exception as e:
        logger.error(f"Erro na simulação de voz: {e}")
        return {"error": f"Erro ao processar: {str(e)}"}


@router.post("/inbound")
async def voice_inbound(
    From: str = Form(...),
    To: str = Form(...),
    CallSid: str = Form(...),
    agent_id: str | None = Form(None),
    conversation_id: str | None = Form(None),
):
    phone = From.replace("+", "")

    async with AsyncSessionLocal() as db:
        if agent_id:
            result = await db.execute(select(Agent).where(Agent.id == agent_id))
        else:
            result = await db.execute(select(Agent).where(Agent.phone_number == To))
        agent = result.scalar_one_or_none()
        if not agent:
            twiml = voice_service.create_callback_twiml(
                "Desculpe, não consegui atender sua chamada."
            )
            return Response(content=twiml, media_type="application/xml")

        contact_result = await db.execute(
            select(Contact).where(Contact.phone == phone, Contact.tenant_id == agent.tenant_id),
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

    twiml = voice_service.create_inbound_twiml(
        agent_id=str(agent.id),
        conversation_id=str(conversation.id),
    )
    return Response(content=twiml, media_type="application/xml")


@router.post("/speech-result")
async def voice_speech_result(
    SpeechResult: str = Form(""),
    CallSid: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
    agent_id: str | None = Form(None),
    conversation_id: str | None = Form(None),
):
    phone = From.replace("+", "")

    try:
        async with AsyncSessionLocal() as db:
            if agent_id:
                result = await db.execute(select(Agent).where(Agent.id == agent_id))
            else:
                result = await db.execute(select(Agent).where(Agent.phone_number == To))
            agent = result.scalar_one_or_none()
            if not agent:
                twiml = voice_service.create_callback_twiml("Desculpe, ocorreu um erro.")
                return Response(content=twiml, media_type="application/xml")

            contact_result = await db.execute(
                select(Contact).where(Contact.phone == phone, Contact.tenant_id == agent.tenant_id),
            )
            contact = contact_result.scalar_one_or_none()

            if conversation_id:
                conv_result = await db.execute(
                    select(Conversation).where(Conversation.id == conversation_id)
                )
            else:
                conv_result = await db.execute(
                    select(Conversation).where(
                        Conversation.agent_id == agent.id,
                        Conversation.contact_id == contact.id if contact else False,
                        Conversation.channel == "voice",
                        Conversation.status == "active",
                    ),
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
                .limit(20),
            )
            history = [
                {"role": m.role, "content": m.content} for m in reversed(hist_result.scalars().all())
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

        twiml = voice_service.create_speech_response(
            ai_response,
            continue_listening=True,
            agent_id=agent_id,
            conversation_id=str(conversation.id),
        )
        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Erro no speech-result: {e}")
        twiml = voice_service.create_speech_response(
            "Desculpe, tive um problema técnico. Pode repetir?",
            continue_listening=True,
        )
        return Response(content=twiml, media_type="application/xml")


@router.post("/outbound")
async def voice_outbound(to: str, agent_id: str, message: str = ""):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if not agent:
            return {"error": "Agente não encontrado"}

        url = f"{settings.TWILIO_WEBHOOK_URL}/api/v1/voice/inbound?agent_id={agent_id}"
        call_result = voice_service.make_call(to=to, url=url)
        return {"status": "calling", "call_sid": call_result["call_sid"]}


@router.post("/status")
async def voice_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    CallDuration: str = Form(None),
):
    logger.info(f"Status da chamada {CallSid}: {CallStatus} (duração: {CallDuration}s)")

    if CallStatus in ("completed", "failed", "busy", "no-answer", "canceled"):
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(Conversation).where(
                        Conversation.channel == "voice",
                        Conversation.status == "active",
                    ).order_by(Conversation.created_at.desc()).limit(1)
                )
                conversation = result.scalar_one_or_none()
                if conversation:
                    conversation.status = "closed"
                    if CallDuration:
                        conversation.metadata = conversation.metadata or {}
                        conversation.metadata["call_duration"] = int(CallDuration)
                        conversation.metadata["call_sid"] = CallSid
                        conversation.metadata["call_status"] = CallStatus
                    await db.commit()
                    logger.info(f"Conversa {conversation.id} fechada (chamada {CallStatus})")
        except Exception as e:
            logger.error(f"Erro ao fechar conversa no status callback: {e}")

    return Response(status_code=200)
