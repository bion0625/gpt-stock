from celery.schedules import crontab
from celery import Celery
from app.tasks import update_all_stocks as update_all_stocks_async
import asyncio

celery_app = Celery(
    'gpt_stock',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Seoul',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'update-stocks-every-day' : {
        'task': 'app.celery_worker.update_all_stocks',
        'schedule': crontab(hour=22, minute=0),
        # 'schedule': crontab(minute='*/1'), # TEST 매 1분마다 실행
    },
}

@celery_app.task
def update_all_stocks():
    asyncio.run(update_all_stocks_async())