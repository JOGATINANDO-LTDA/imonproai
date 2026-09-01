import logging
from datetime import UTC, datetime

from sqlalchemy import func, select

from app.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.base import Contact

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.analytics.generate_daily_metrics")
async def generate_daily_metrics():
    async with AsyncSessionLocal() as db:
        now = datetime.now(UTC)

        result = await db.execute(
            select(
                Contact.tenant_id,
                func.count(Contact.id).label("total_contacts"),
            ).group_by(Contact.tenant_id),
        )
        tenant_stats = result.all()

        logger.info(f"Métricas diárias geradas para {len(tenant_stats)} tenants")

    return {"status": "completed", "tenants_processed": len(tenant_stats)}
