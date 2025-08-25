# app/config.py
from kombu import Exchange, Queue

BROKER_URL =  "amqp://guest:guest@rabbitmq:5672//" 
RESULT_BACKEND = "redis://redis:6379/0"              # Redis

CELERY_TASK_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("priority", Exchange("priority"), routing_key="priority"),
)

CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
CELERY_TASK_DEFAULT_ROUTING_KEY = "default"
CELERY_TASK_ACKS_LATE = True  # اطمینان از عدم گم شدن job
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # مصرف بهینه RAM
