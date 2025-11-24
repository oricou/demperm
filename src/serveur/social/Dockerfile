FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    cargo \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh
RUN mkdir -p api/logs api/staticfiles api/media

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["gunicorn", "--chdir", "/app/api", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "conf.wsgi:application"]
