import logging
from datetime import UTC, datetime

from sqlalchemy import select

from app.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.integrations.email import EmailService
from app.integrations.whatsapp import WhatsAppService
from app.models.base import Contact, FollowUp

logger = logging.getLogger(__name__)

email_service = EmailService()
whatsapp_service = WhatsAppService()


@celery_app.task(name="app.tasks.follow_ups.process_pending_follow_ups")
async def process_pending_follow_ups():
    now = datetime.now(UTC)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(FollowUp).where(
                FollowUp.status == "pending",
                FollowUp.scheduled_at <= now,
            ),
        )
        follow_ups = result.scalars().all()

        for follow_up in follow_ups:
            try:
                contact_result = await db.execute(
                    select(Contact).where(Contact.id == follow_up.contact_id),
                )
                contact = contact_result.scalar_one_or_none()
                if not contact:
                    follow_up.status = "failed"
                    continue

                if follow_up.channel == "whatsapp" and contact.whatsapp:
                    # TODO: Send via WhatsApp
                    follow_up.status = "sent"
                elif follow_up.channel == "email" and contact.email:
                    await email_service.send_email(
                        to=contact.email,
                        subject="Lembrete da ImobPro.ai",
                        html_body=f"<p>{follow_up.message}</p>",
                    )
                    follow_up.status = "sent"
                else:
                    follow_up.status = "failed"
                    logger.warning(f"Follow-up {follow_up.id}: canal/tipo de contato indisponível")

            except Exception as e:
                logger.error(f"Erro ao processar follow-up {follow_up.id}: {e}")
                follow_up.status = "failed"

        await db.commit()

    return {"processed": len(follow_ups)}
