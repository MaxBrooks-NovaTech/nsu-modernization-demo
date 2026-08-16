#!/usr/bin/env bash
set -euo pipefail

python3 scripts/generate_synthetic_data.py
docker compose down -v
docker compose up -d
docker compose exec -T postgres sh -c 'until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do sleep 1; done'
bash scripts/validate_phase1.sh
