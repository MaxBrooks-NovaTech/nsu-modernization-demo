# Setup

## Prerequisites

- Docker Desktop
- Python 3
- Git
- Power BI Desktop only if creating native PBIP output manually on Windows

## Local setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
python3 scripts/generate_synthetic_data.py
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
```

The reset script recreates the local Docker volume, initializes the `raw` schema, loads deterministic CSV seed data, and runs Phase 1 validation. It is destructive to the local demonstration database only.

## dbt validation

```bash
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt debug --project-dir . --profiles-dir .
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir . --no-use-colors
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors
```

Expected current result: 11/11 source freshness checks pass and 62/62 dbt build nodes pass with zero errors and warnings.

## Port override

The compose default is host port `5432`. If occupied, use `POSTGRES_PORT=55432` consistently for reset, dbt, and direct database commands.

## Safety

All data is synthetic. Do not add real NSU data, credentials, production connection strings, or persistent production integrations.
