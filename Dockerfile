FROM python:3.11.1-slim



WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--workers","9"]
CMD ["fastapi","dev","main.py","--host", "0.0.0.0", "--port", "8000"]
