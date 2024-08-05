#!/bin/bash

set -e

echo "Stopping all containers..."
docker compose down

echo "Creating external volumes if they don't exist..."
docker volume create --name=postgres_data || true
docker volume create --name=minio_data || true
docker volume create --name=qdrant_data || true

echo "Resetting data..."
docker compose -f docker-compose.reset.yml up --build

echo "Removing old containers and volumes..."
docker compose down -v

echo "Starting services with fresh data..."
docker compose up -d

echo "Running database migrations..."
docker compose exec -e POSTGRES_USER -e POSTGRES_PASSWORD -e POSTGRES_DB fastapi-app alembic upgrade head

echo "Creating new migration if needed..."
docker compose exec -e POSTGRES_USER -e POSTGRES_PASSWORD -e POSTGRES_DB fastapi-app alembic revision --autogenerate -m "Auto-generated migration" || true

echo "Applying any new migrations..."
docker compose exec -e POSTGRES_USER -e POSTGRES_PASSWORD -e POSTGRES_DB fastapi-app alembic upgrade head

echo "Reset complete. Your environment is now fresh and updated."
