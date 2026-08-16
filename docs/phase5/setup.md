# Phase 5 — Power BI / PBIP

Phase 5 delivers the Power BI layer for the three required interview report experiences: Executive Enrollment & Admissions, Institutional Data Trust, and Data Lineage & Certification.

## Purpose & Scope

1. **Source-controlled report specifications**: `powerbi/*/report-spec.yml` define each report's source models, semantic definitions, pages, visuals, and slicers as reviewable, version-controlled YAML — independent of whether Power BI Desktop is available.
2. **Native PBIP project**: `powerbi/NSU BI Modernization Demo/` is a real Power BI Project (`.pbip` + `.Report` + `.SemanticModel`, TMDL format) built in Power BI Desktop on Windows, since Power BI Desktop is unavailable on macOS.
3. **Portable data source**: the semantic model can source from either the live local PostgreSQL marts or the exported CSV snapshots in `seeds/mart_tables/`, so the Power BI portion of the demo does not require Docker/PostgreSQL to be running.

## Core Artifacts

- `powerbi/README.md` — index and manual-step documentation.
- `powerbi/executive-enrollment-admissions/report-spec.yml`, `powerbi/institutional-data-trust/report-spec.yml`, `powerbi/data-lineage-certification/report-spec.yml` — per-report specifications.
- `powerbi/NSU BI Modernization Demo/` — the native PBIP project (semantic model + report pages).
- `seeds/mart_tables/*.csv` — CSV exports of the three certified marts for a Postgres-free Power BI connection.

## Governed Metrics Represented

The semantic model's DAX measures are written to match `semantic/metric_definitions.yml`'s `calculation` field exactly (not approximated): `Enrolled`, `Applications`, `Admits`, `Deposits`, `Yield`, `CensusEnrollment`, `IpedsEnrollment`.

## Known Limitations

- Power BI Desktop is unavailable on macOS; the native PBIP project must be opened, refreshed, and have its visuals built/verified on Windows.
- No native `.pbix` or rendered screenshots are claimed as validated until a human has completed that step in real Power BI Desktop.

## How to Run & Verify Phase 5

```bash
# Validate the report specifications are well-formed YAML
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('powerbi/*/report-spec.yml')]; print('OK')"

# Refresh the CSV snapshot the PBIP semantic model can read without Postgres running
POSTGRES_PORT=55432 bash scripts/export_mart_csvs.sh
```
