# Interview Demo Runbook

## Goal

Demonstrate that governance is QA for data, certification is a release gate, and a governed model can be reused across decisions.

## Before the demo

- Use synthetic data only.
- Confirm Docker Desktop is running.
- If port `5432` is occupied, use `POSTGRES_PORT=55432`.
- Do not use NSU credentials, production connection strings, or real data.

## Walkthrough

1. Explain the problem: disconnected reports and conflicting institutional definitions.
2. Show the architecture and the conceptual Banner/SQL Server boundary in `docs/architecture.md`.
3. Generate deterministic data and start/reset PostgreSQL:
   ```bash
   python3 scripts/generate_synthetic_data.py
   POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
   ```
4. Run the quality and transformation release checks:
   ```bash
   POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir . --no-use-colors
   POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors
   ```
5. Explain `FactEnrollment` grain: one student registration, one section, one academic term.
6. Show `semantic/metric_definitions.yml` and explain why Applications, Admits, Deposits, Enrolled, Yield, Census Enrollment, and IPEDS Enrollment are separate governed questions.
7. Show `contracts/fact_enrollment.yml`, `certification/catalog.yml`, and the passing test evidence.
8. Walk through `docs/phase4/lineage.md`: source, transformation, certified model, semantic definition, and report.
9. Demonstrate change control with a ready-made breaking scenario:
   ```bash
   tmp=$(mktemp -d)
   cp contracts/fact_enrollment.yml "$tmp/before.yml"
   cp contracts/fact_enrollment.yml "$tmp/after.yml"
   python3 - <<'PY' "$tmp/after.yml"
   from pathlib import Path
   import sys
   path = Path(sys.argv[1])
   text = path.read_text()
   text = text.replace('  - registration_id\n', '')
   path.write_text(text)
   PY
   python3 scripts/check_contract_changes.py "$tmp/before.yml" "$tmp/after.yml"
   rm -rf "$tmp"
   ```
   The command must fail with a breaking required-field removal. A required-field, grain, quality-rule, or certified-metric logic change must fail the check.
10. Open the three `powerbi/*/report-spec.yml` files. Explain that these are source-controlled report specifications; native PBIP generation is a documented manual Power BI Desktop step on Windows and is not claimed on macOS.
11. Close with the decision: build once, reuse many times, with trust and release evidence.

## Interview talking points

- Modernization is incremental: preserve source-system ownership, create a governed foundation, then retire duplicated reporting logic over time.
- Security comes before touching production student data; this demo stays synthetic and isolated.
- Conflicting numbers are resolved by certified definitions and explicit grain, not by forcing every metric to be identical.
- Cost and ROI are governed decisions: start with a small reproducible foundation and measure reuse, quality, and report retirement.

## Known limitations

- The database is a local demonstration PostgreSQL instance, not NSU production.
- Power BI Desktop is unavailable in the current macOS environment; report specifications are real repository artifacts, but native `.pbip`, `.pbix`, and screenshots are not present.
- No live cloud metadata, Fabric, Purview, authentication, or production integration is included.
