#!/bin/bash
set -e

echo "Seeding users..."
python /app/seed_users.py

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
