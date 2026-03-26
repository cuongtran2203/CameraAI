# =====================================================
# CameraAI — Main FastAPI Backend
# =====================================================

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# ── System dependencies ──────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ──────────────────────────────
COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# ── Application code ─────────────────────────────────
COPY app/ ./app/
COPY seed_users.py ./
COPY entrypoint.sh ./

# ── Entrypoint ───────────────────────────────────────
EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
