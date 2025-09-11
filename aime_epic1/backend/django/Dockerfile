# backend/django/Dockerfile  (mysqlclient)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive

# Build deps for mysqlclient on Debian slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3-dev \
      build-essential \
      gcc \
      default-libmysqlclient-dev \
      libmariadb-dev-compat \
      pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip toolchain first, then install Python deps
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# App code
COPY . /app

EXPOSE 8000