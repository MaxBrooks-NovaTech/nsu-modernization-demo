# Phase 6 — Documentation & Demo

Phase 6 delivers the documentation and demo runbook that make the rest of the project usable and defensible without narration.

## Purpose & Scope

1. **Architecture**: `docs/architecture.md` — end-to-end flow, certified products, governance controls, and explicit boundaries.
2. **Setup**: `docs/setup.md` — reproducible local setup from a clean machine.
3. **Data dictionary**: `docs/data-dictionary.md` — column-level reference for the three certified marts (source, type, description, nullability, test coverage).
4. **Demo runbook**: `docs/demo.md` — the walkthrough, including a ready-to-run breaking-change example. Local-only; not tracked in git (see `.gitignore`).
5. **Visual evidence**: `docs/images/` — screenshots of the dbt docs site (model graph, column descriptions, semantic layer) and the loaded PostgreSQL tables, so the governed model and column-level documentation are visible without a live walkthrough.

## Core Artifacts

- `docs/architecture.md`, `docs/setup.md`, `docs/data-dictionary.md` (tracked); `docs/demo.md` (local-only)
- `docs/images/` — dbt docs and PostgreSQL screenshots (see `docs/images/README.md` for what each file shows and how it was generated)
- README's "Documentation and Demo" section, linking all of the above

## How to Run & Verify Phase 6

```bash
# Reproduce the documented setup from a clean state
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir . --no-use-colors
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors

# Regenerate the dbt docs site (source for the docs/images screenshots)
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt docs generate --project-dir . --profiles-dir .
POSTGRES_PORT=55432 .venv/bin/dbt docs serve --project-dir . --profiles-dir . --port 8180
```

_Expected result_: 11/11 source freshness checks pass, 62/62 dbt build nodes pass with 0 errors/warnings, and the dbt docs site serves at `http://localhost:8180` showing the model graph, column-level descriptions from `models/marts/schema.yml`, and test coverage per model.
