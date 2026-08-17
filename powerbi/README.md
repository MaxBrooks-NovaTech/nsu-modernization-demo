# Phase 5 — Power BI / PBIP

This directory contains both the source-controlled Power BI report specifications and a real native PBIP project for this demonstration.

## Contents

1. `executive-enrollment-admissions/`, `institutional-data-trust/`, `data-lineage-certification/` — `report-spec.yml` specifications for the three required report experiences (source models, semantic definitions, pages, visuals, slicers).
2. `NSU BI Modernization Demo/` — the native PBIP project (`.pbip` + `.Report` + `.SemanticModel`, TMDL format), built in Power BI Desktop on Windows since Power BI Desktop is unavailable on macOS.

## Data source: OneLake Lakehouse `NSU_DEMO`

The Power BI semantic model imports its fact tables, dimension tables, and governance/reference tables from the OneLake Lakehouse named **`NSU_DEMO`**. The Lakehouse is the Power BI consumption layer for this demonstration and is intentionally separate from NSU production systems.

### Imported fact tables

- `FactEnrollment` — one row per student registration in one section for one academic term.
- `RecruitmentFunnel` — one row per application with admission and deposit outcomes.
- `CensusEnrollment` — one row per student-term census record.

### Imported dimension tables

- `dim_school` — school names and codes used by slicers and chart axes.
- `dim_program` — program names, degree levels, and CIP codes used by slicers and analysis.
- `dim_term` — academic term names, academic years, and dates used by slicers and time analysis.

The fact and dimension tables are related through their documented keys: `school_id`, `program_id`, and `term_id`. The semantic model uses active, single-direction, many-to-one relationships from each fact table to the corresponding dimension table.

### Imported governance/reference tables

The Institutional Data Trust and Data Lineage & Certification pages also import these tables from `NSU_DEMO`:

- `CertificationCatalog`
- `LineageSummary`
- `QualityTestEvidence`

These tables are generated from the certification catalog, lineage documentation, and actual dbt test results before being loaded into the Lakehouse. They are governance evidence, not illustrative sample data.

The local CSV files under `seeds/mart_tables/` and `seeds/dimension_tables/` are reproducible synthetic-data exchange snapshots used to populate or refresh `NSU_DEMO`. They are not the Power BI report's intended production connection. Docker/PostgreSQL is used upstream to generate and validate the demonstration data; Power BI consumes the resulting Lakehouse tables.

To refresh the source snapshots after re-running `dbt build`:

```bash
POSTGRES_PORT=55432 bash scripts/export_mart_csvs.sh
python3 scripts/export_dashboard_reference_csvs.py
python3 scripts/export_onelake_dimension_tables.py
```

Upload the refreshed CSV outputs to the appropriate tables in the `NSU_DEMO` Lakehouse, then refresh the Power BI semantic model. `scripts/export_dashboard_reference_csvs.py` regenerates `CertificationCatalog`, `LineageSummary`, and `QualityTestEvidence` from `certification/catalog.yml`, `docs/phase4/lineage.md`, and `target/run_results.json`.

## Governed metrics

The model's DAX measures (`Enrolled`, `Applications`, `Admits`, `Deposits`, `Yield`, `CensusEnrollment`, `IpedsEnrollment`) are written to match `semantic/metric_definitions.yml`'s `calculation` field for each metric exactly — not approximated with unfiltered row counts.

## Remaining manual Power BI Desktop step

The three report pages (`Executive Enrollment & Admissions`, `Institutional Data Trust`, `Data Lineage & Certification`) exist and are navigable, but their visuals (cards, charts, tables, slicers) still need to be built in Power BI Desktop per each `report-spec.yml`. This is GUI-authored work that cannot be done from a text edit — build it, then validate against the Phase 3 dbt marts and Phase 4 certification catalog before presenting.

See `PowerBIDashboard.md` (repository root) for the exact step-by-step checklist — connecting the report to the `NSU_DEMO` Lakehouse, validating the fact and dimension tables, and building each page.
