# Phase 7 — Final QA

Phase 7 is the final, whole-project verification pass before the demonstration is presented — reproducibility, correctness, and honesty checks across every prior phase, without expanding scope.

## Purpose & Scope

1. **Reproducibility**: deterministic synthetic-data regeneration, a clean PostgreSQL reset/load, and a full `dbt build` from that clean state.
2. **Governance mechanics**: contract change detection, including a real intentional breaking-change scenario, not just a description of one.
3. **Power BI artifact correctness**: the native PBIP semantic model's connection details, column types, and DAX measures are checked against the actual running database and `semantic/metric_definitions.yml`, not just assumed correct because the files exist.
4. **Documentation and repository safety**: every documented link resolves, no real NSU data or credentials are tracked, and every phase's claims are evidenced rather than asserted.

## How to Run & Verify Phase 7

```bash
# Determinism
python3 scripts/generate_synthetic_data.py
sha256sum seeds/*.csv > /tmp/seeds_before.txt
python3 scripts/generate_synthetic_data.py
sha256sum seeds/*.csv > /tmp/seeds_after.txt
diff /tmp/seeds_before.txt /tmp/seeds_after.txt && echo "Deterministic: seed hashes identical"

# Clean-state pipeline
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt debug --project-dir . --profiles-dir .
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir . --no-use-colors
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors

# Contract change detection — unchanged and intentional-break scenarios
python3 scripts/check_contract_changes.py contracts/fact_enrollment.yml contracts/fact_enrollment.yml
```

_Expected result_: identical seed hashes, `dbt debug` OK, 11/11 freshness checks, 62/62 build nodes with 0 errors/warnings, and `No breaking contract changes detected.` for the unchanged-contract comparison.

## Known Limitation

Power BI Desktop is unavailable on macOS, so native interactive rendering and visual authoring for `powerbi/NSU BI Modernization Demo/` were not executed in this environment. The semantic model's connection string, column types, and certified-metric DAX formulas were independently checked against the real database and `semantic/metric_definitions.yml` and corrected where wrong; the report pages' visuals still require a human with Power BI Desktop access to build and verify. No fabricated rendering, screenshots, or artifacts are claimed — see `docs/handoff/claude-review.md` ("PHASE 7 FINAL QA REVIEW") for the full verification record.
