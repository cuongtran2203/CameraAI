# Use official slim Python 3.10 image (Required for PyTorch 2.5 wheels)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu128 torch \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy all files from the context (./app/ai_service) into /app
COPY . .

# Ensure images/ dir exists (StaticFiles requires it)
RUN mkdir -p /app/ai_service/images

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]