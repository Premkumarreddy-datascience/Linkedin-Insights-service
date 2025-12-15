FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app



CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
