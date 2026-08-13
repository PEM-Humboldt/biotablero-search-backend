# Build stage
FROM python:3.10-slim-bookworm AS builder

## Configure environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

## Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

## Create and enable virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

## Install Python dependencies
WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Runtime stage
FROM python:3.10-slim-bookworm AS runner

## Configure environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    HOST=0.0.0.0

## Install system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libexpat1 \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

## User setup
RUN groupadd -g 10001 app && \
    useradd -u 10001 -g app -s /bin/bash -m app

## Copy builded project
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

## Make logs directory
RUN mkdir -p /app/logs && \
    chown -R app:app /app

## Copy application code
COPY --chown=app:app . /app

# Cambiar a usuario no-root
USER app

## Open port
EXPOSE 8000

## Docker health check setup
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/docs > /dev/null || curl -fsS http://localhost:${PORT}/areas/types > /dev/null || exit 1

## Execute program
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${PORT}"]
