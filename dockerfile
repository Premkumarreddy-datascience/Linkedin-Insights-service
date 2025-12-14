FROM python:3.10-bullseye

WORKDIR /app

ENV PIP_ONLY_BINARY=:all:
ENV PIP_NO_BUILD_ISOLATION=1

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
