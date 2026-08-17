# Phase 5 — Power BI

This directory contains the source-controlled Power BI report specifications and a native PBIP project for this demonstration. There are currently **two separate Power BI artifacts** in `NSU BI Modernization Demo/New/NSU BI Modernization Demo New/`, on two different data-source strategies — read the "Two artifacts" section below before editing either one.

## Contents

1. `executive-enrollment-admissions/`, `institutional-data-trust/`, `data-lineage-certification/` — `report-spec.yml` specifications for the three required report experiences (source models, semantic definitions, pages, visuals, slicers).
2. `NSU BI Modernization Demo/New/NSU BI Modernization Demo New/` — the native PBIP project (`.pbip` + `.Report` + `.SemanticModel`, TMDL format) and the `.pbix` file.

## Two artifacts, two data-source strategies

- **`NSU BI Modernization Demo.pbix`** — the primary, live artifact. Connected to the **`nsu_demo` Fabric Lakehouse's SQL analytics endpoint** (`e24kd4t5iotezbksgc6j5zwpeq-ctcxpmaaogturcuygmjtlcx4hy.datawarehouse.fabric.microsoft.com`, Lakehouse/SQL-endpoint name `nsu_demo`). All tables at the SQL endpoint are **snake_case**, matching the dbt mart/seed naming convention (see table list below). As of 2026-08-17 this file has no visuals built yet — it still has Power BI Desktop's default blank "Page 1"; the three governed report pages haven't been created in it.
- **`NSU BI Modernization Demo.pbip`** (+ `.Report` + `.SemanticModel`, TMDL) — a portable, offline fallback that imports the same data directly from this repo's `seeds/*.csv` files (no Fabric tenant required to open it). It went through a structural repair on 2026-08-17 — the version checked in before that date had a fabricated report definition (a non-schema `visuals` array standing in for real visual containers) and systemically malformed TMDL in every table file, both of which blocked Power BI Desktop from opening it at all. That repair is logged in `docs/handoff/claude-review.md` ("Fourth Follow-Up"). Its tables are now named `fact_enrollment`, `fact_recruitment_funnel`, `fact_census_enrollment`, `dim_school`, `dim_program`, `dim_term`, `certification_catalog`, `lineage_summary`, `quality_test_evidence` — all snake_case, matching the naming convention at the live SQL endpoint. Reconciling the `.pbip`'s TMDL model to connect to the real SQL endpoint (rather than local CSVs) is a semantic-model change that hasn't been done — see "Reconciling the two artifacts" below.

**Neither file has its report visuals built yet.** Instructions for building them live in `PowerBIVisualizationInstructions.md` (repository root) — written against the `.pbip`'s existing 3-page structure and local-CSV field names; the field/measure/visual guidance applies conceptually to the `.pbix` too, but the three pages need to be created there from scratch (it currently only has the default blank page) and the table/field names in the instructions should be read as their snake_case SQL-endpoint equivalents. Ask if you'd like that file rewritten specifically against the `.pbix`.

## Data source

### Live: Fabric Lakehouse SQL endpoint (`.pbix`)

- **Lakehouse / SQL endpoint name:** `nsu_demo`
- **SQL analytics endpoint:** `e24kd4t5iotezbksgc6j5zwpeq-ctcxpmaaogturcuygmjtlcx4hy.datawarehouse.fabric.microsoft.com`
- **Connectivity:** Power BI Desktop → Get Data → SQL Server (or the Lakehouse connector pointed at the SQL analytics endpoint), authenticated against the Fabric workspace.

#### Tables (snake_case, as they exist at the SQL endpoint)

- `fact_enrollment` — one row per student registration in one section for one academic term.
- `fact_recruitment_funnel` — one row per application with admission and deposit outcomes.
- `fact_census_enrollment` — one row per student-term census record.
- `dim_school` — school names and codes used by slicers and chart axes.
- `dim_program` — program names, degree levels, and CIP codes used by slicers and analysis.
- `dim_term` — academic term names, academic years, and dates used by slicers and time analysis.
- `certification_catalog` — certification/ownership/status metadata per certified data product.
- `lineage_summary` — source-to-consumer lineage per certified data product.
- `quality_test_evidence` — real dbt test results (pass/fail + evidence) backing each certification.

The fact and dimension tables relate on `school_id`, `program_id`, and `term_id`. Reference the SQL endpoint's actual live schema as authoritative if anything here drifts — this list is current as of 2026-08-17 per direct confirmation, not introspected from the (binary, not text-diffable) `.pbix` file itself.

### Portable fallback: local CSV import (`.pbip`)

Every table in the `.pbip`'s semantic model is Power Query **Import mode**, reading directly from the CSVs checked into this repo under `seeds/mart_tables/` and `seeds/dimension_tables/`, using the `ProjectRoot` M parameter (`NSU BI Modernization Demo.SemanticModel/definition/model.tmdl`) to build each file path. A `LakehouseName` parameter and `SourceSystem = "OneLake Lakehouse NSU_DEMO"` annotations exist on each table but aren't wired to a real connector in any partition's M code — they're placeholders for the reconciliation described below, not evidence of a live connection in this file. **To open and refresh this project on your own machine:** set the `ProjectRoot` parameter (Transform data → Manage Parameters, or edit `model.tmdl` directly) to the absolute path of your local clone of this repository, then Refresh.

To refresh the source CSVs after re-running `dbt build`:

```bash
POSTGRES_PORT=55432 bash scripts/export_mart_csvs.sh
python3 scripts/export_dashboard_reference_csvs.py
python3 scripts/export_onelake_dimension_tables.py
```

`scripts/export_dashboard_reference_csvs.py` regenerates `certification_catalog.csv`, `lineage_summary.csv`, and `quality_test_evidence.csv` from `certification/catalog.yml`, `docs/phase4/lineage.md`, and `target/run_results.json`.

### Reconciling the two artifacts

The `.pbip`'s TMDL model could be pointed at the same `nsu_demo` SQL endpoint (swapping each table's `source` step from `Csv.Document(File.Contents(ProjectRoot & ...))` to a `Sql.Database("e24kd4t5iotezbksgc6j5zwpeq-ctcxpmaaogturcuygmjtlcx4hy.datawarehouse.fabric.microsoft.com", "nsu_demo")`-style query, and renaming the three PascalCase fact tables to their snake_case equivalents) so only one model needs to be maintained. That hasn't been done — it's a semantic-model change, not a docs fix, and is best done from inside Power BI Desktop where the connection can be authenticated and validated interactively rather than hand-written blind.

## Governed metrics

The model's DAX measures (`Enrolled`, `Applications`, `Admits`, `Deposits`, `Yield`, `CensusEnrollment`, `IpedsEnrollment`) are written to match `semantic/metric_definitions.yml`'s `calculation` field for each metric exactly — not approximated with unfiltered row counts.

## Remaining manual Power BI Desktop step

Neither artifact has its report visuals built yet. See **`PowerBIVisualizationInstructions.md`** (repository root) for the field-by-field, page-by-page checklist — it covers every visual called for in each `report-spec.yml` and flags the two places the visuals need a small judgment call rather than a literal spec reading (the funnel on page 1, the non-existent `release_gate` field on page 2). It was written against the `.pbip`; if you're building directly in the `.pbix` against the live SQL endpoint, translate the table/field names to their snake_case equivalents above. Validate the finished pages against the Phase 3 dbt marts and Phase 4 certification catalog before presenting.
