from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "imobpro",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.follow_ups", "app.tasks.analytics"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "process-follow-ups": {
            "task": "app.tasks.follow_ups.process_pending_follow_ups",
            "schedule": 60.0,
        },
        "generate-daily-metrics": {
            "task": "app.tasks.analytics.generate_daily_metrics",
            "schedule": 3600.0,
        },
    },
)
