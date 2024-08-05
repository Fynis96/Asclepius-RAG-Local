#!/bin/bash

set -e

echo "Stopping all containers..."
docker compose down

echo "Resetting data..."
docker compose -f docker-compose.reset.yml up --build

echo "Removing old containers and volumes..."
docker compose down -v

echo "Starting services with fresh data..."
docker compose up -d

echo "Running database migrations..."
docker compose exec fastapi-app alembic upgrade head

echo "Reset complete. Your environment is now fresh and updated."