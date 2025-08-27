from celery import Celery

app = Celery('crawler')

app.conf.update(
    broker_url='redis://redis:6379/0',
    result_backend='redis://redis:6379/1',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_soft_time_limit=60,
    task_time_limit=120,
    worker_concurrency=4,
    task_default_queue='default',
    result_expires=3600,
    beat_scheduler='celery.beat:PersistentScheduler',
    beat_schedule_filename='celerybeat-schedule',
    beat_max_loop_interval=300,
    beat_schedule={
        'run-every-30-seconds': {
            'task': 'save_user_data',
            'schedule': 10.0,
        }
    }
)
import requests
from main import get_db,User
@app.task(name='save_user_data')
def save_user_data():
    limit = 100
    offset = 0

    with get_db() as db:
        offset = db.query(User).all()
        if offset:
            offset = offset[-1].user_id
        else:
            offset = 0
        payload = {
            "limit":limit,
            "offset": offset
        }
        response = requests.get('http://2.179.194.90/user_data/',params=payload)
        users_to_add = [
        User(
            username=user_data.get("username"),
            password=user_data.get("password"),
            user_id=user_data.get("user_id")
        )
        for user_data in response.json()
        ]
    
        db.add_all(users_to_add)
        db.commit()
        print(offset)