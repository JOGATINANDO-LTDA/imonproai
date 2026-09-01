import logging

from fastapi import APIRouter, Request, Response
from sqlalchemy import select

from app.agent.engine import ImobProAgent
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.integrations.whatsapp import WhatsAppService
from app.models.base import Agent, Contact, Conversation, Message

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

whatsapp_service = WhatsAppService()


@router.post("/whatsapp/{instance}")
async def whatsapp_webhook(instance: str, request: Request):
    body = await request.json()
    event = body.get("event")
    data = body.get("data", {})

    if event not in ("messages.upsert", "message-receipt.update"):
        return Response(status_code=200)

    message_data = data
    if not message_data:
        return Response(status_code=200)

    key = message_data.get("key", {})
    from_me = key.get("fromMe", False)
    if from_me:
        return Response(status_code=200)

    phone = key.get("remoteJid", "").replace("@s.whatsapp.net", "")
    conversation_id = key.get("id", "")
    message_content = message_data.get("message", {})

    text = ""
    content_type = "text"
    if "conversation" in message_content:
        text = message_content["conversation"]
    elif "extendedTextMessage" in message_content:
        text = message_content["extendedTextMessage"].get("text", "")
    elif "imageMessage" in message_content:
        text = message_content["imageMessage"].get("caption", "[Imagem recebida]")
        content_type = "image"
    elif "audioMessage" in message_content:
        text = "[Áudio recebido]"
        content_type = "audio"
    elif "documentMessage" in message_content:
        text = f"[Documento: {message_content['documentMessage'].get('fileName', 'arquivo')}]"
        content_type = "document"

    if not text:
        return Response(status_code=200)

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(Agent).where(Agent.whatsapp_instance == instance))
            agent = result.scalar_one_or_none()
            if not agent:
                logger.warning(f"Agente não encontrado para instance: {instance}")
                return Response(status_code=200)

            contact_result = await db.execute(
                select(Contact).where(
                    Contact.whatsapp == phone, Contact.tenant_id == agent.tenant_id
                ),
            )
            contact = contact_result.scalar_one_or_none()
            if not contact:
                contact = Contact(
                    tenant_id=agent.tenant_id,
                    name=phone,
                    whatsapp=phone,
                    status="new",
                )
                db.add(contact)
                await db.flush()

            conv_result = await db.execute(
                select(Conversation).where(
                    Conversation.contact_id == contact.id,
                    Conversation.agent_id == agent.id,
                    Conversation.status == "active",
                ),
            )
            conversation = conv_result.scalar_one_or_none()
            if not conversation:
                conversation = Conversation(
                    agent_id=agent.id,
                    contact_id=contact.id,
                    channel="whatsapp",
                    status="active",
                )
                db.add(conversation)
                await db.flush()

            user_msg = Message(
                conversation_id=conversation.id,
                role="user",
                content=text,
                content_type=content_type,
                extra_data={"phone": phone, "whatsapp_message_id": conversation_id},
            )
            db.add(user_msg)

            hist_result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at.desc())
                .limit(20),
            )
            history = [
                {"role": m.role, "content": m.content}
                for m in reversed(hist_result.scalars().all())
            ]

            from app.models.base import Tenant

            tenant_result = await db.execute(select(Tenant).where(Tenant.id == agent.tenant_id))
            tenant = tenant_result.scalar_one_or_none()

            ai_agent = ImobProAgent(
                tenant_name=tenant.name if tenant else "Imobiliária",
                agent_name=agent.name,
                commercial_rules=tenant.commercial_rules if tenant else "",
                llm_model=agent.llm_model,
            )

            ai_response = await ai_agent.process_message(
                user_message=text,
                channel="whatsapp",
                history=history,
                context={
                    "tenant_id": agent.tenant_id,
                    "contact_id": contact.id,
                    "phone": phone,
                    "contact_name": contact.name,
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

            await whatsapp_service.send_text(instance=instance, to=phone, message=ai_response)

        except Exception as e:
            logger.error(f"Erro ao processar mensagem WhatsApp: {e}")
            await db.rollback()

    return Response(status_code=200)
