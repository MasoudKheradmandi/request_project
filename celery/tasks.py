from celery import Celery
from . import config
import requests
import datetime

celery_app = Celery(
    "fastapi_celery",
    broker=config.BROKER_URL,
    backend=config.RESULT_BACKEND,
)

celery_app.conf.beat_schedule = {
    "call-external-service-every-30-mins": {
        "task": "call_external_service",
        "schedule": 30 * 60,  # هر 1800 ثانیه = نیم ساعت
        "options": {"queue": "default"},
    },
}

@celery_app.task(name="call_external_service")
def call_external_service():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    print(f"[{datetime.datetime.now()}] Sending request to {url}")
    response = requests.get(url)
    print(f"Status: {response.status_code}, Body: {response.text[:50]}")
    return {"status": response.status_code, "data": response.json()}
