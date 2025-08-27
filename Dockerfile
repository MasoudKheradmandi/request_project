FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# پیش‌فرض اجرای Celery Worker
CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=INFO"]
