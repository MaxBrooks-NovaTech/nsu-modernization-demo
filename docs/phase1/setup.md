# Phase 1 Setup

Phase 1 creates a local PostgreSQL source-data foundation with deterministic
synthetic data. It is not connected to any NSU production system.

## Generate Seeds

```bash
python3 scripts/generate_synthetic_data.py
```

## Start PostgreSQL

```bash
docker compose up -d
```

On first startup, PostgreSQL creates the `raw` schema and loads CSV files from
`seeds/`.

If the default host port `5432` is already in use, override the host port for
all Compose and lifecycle commands. For example:

```bash
POSTGRES_PORT=55432 docker compose up -d
POSTGRES_PORT=55432 bash scripts/validate_phase1.sh
```

Use the same `POSTGRES_PORT` value for reset operations:

```bash
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
```

## Validate

```bash
bash scripts/validate_phase1.sh
```

## Reset

```bash
bash scripts/reset_phase1.sh
```

The reset script regenerates deterministic seeds, removes the Docker volume,
starts PostgreSQL, waits for readiness, and runs validation.
