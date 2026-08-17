# Phase 5 — Power BI / PBIP

This directory contains both the source-controlled Power BI report specifications and a real native PBIP project for this demonstration.

## Contents

1. `executive-enrollment-admissions/`, `institutional-data-trust/`, `data-lineage-certification/` — `report-spec.yml` specifications for the three required report experiences (source models, semantic definitions, pages, visuals, slicers).
2. `NSU BI Modernization Demo/New/NSU BI Modernization Demo New/` — the native PBIP project (`.pbip` + `.Report` + `.SemanticModel`, TMDL format), built and edited in Power BI Desktop on Windows.

## Current status (as of 2026-08-17)

The PBIP project opens correctly in Power BI Desktop and the semantic model refreshes with real, governed data. It went through a structural repair on 2026-08-17 — the version checked in before that date had a fabricated report definition (a non-schema `visuals` array standing in for real visual containers) and systemically malformed TMDL in every table file, both of which blocked Power BI Desktop from opening the project at all. Full findings and fixes are logged in `docs/handoff/claude-review.md` ("Fourth Follow-Up").

What's still outstanding: **the three report pages have no visuals placed yet.** Building them is GUI-only work that has to happen inside Power BI Desktop (visual containers aren't hand-editable text the way the rest of this project is). Step-by-step instructions for every visual on every page live in `PowerBIVisualizationInstructions.md` (repository root).

## Data source: local CSV import (not a live OneLake/Fabric connection)

Every table in the semantic model (`FactEnrollment`, `RecruitmentFunnel`, `CensusEnrollment`, `dim_school`, `dim_program`, `dim_term`, `certification_catalog`, `lineage_summary`, `quality_test_evidence`) is Power Query **Import mode**, reading directly from the CSVs checked into this repo under `seeds/mart_tables/` and `seeds/dimension_tables/`, using the `ProjectRoot` M parameter (`NSU BI Modernization Demo.SemanticModel/definition/model.tmdl`) to build each file path. There is no live connection to a Fabric OneLake Lakehouse in this project today — a `LakehouseName` parameter exists in `model.tmdl` and each table's `SourceSystem` annotation reads `"OneLake Lakehouse NSU_DEMO"`, but neither is wired to an actual Fabric/OneLake connector in any partition's M code. This matches `docs/architecture.md`'s own framing: Fabric/OneLake is documented as a **conceptual, not live, integration point** for this demonstration (see its "Boundaries" section) — this PBIP is intentionally the portable, no-Fabric-tenant-required version of that.

If a real `NSU_DEMO` Lakehouse is provisioned later, the tables' `SourceSystem` annotations and the unused `LakehouseName` parameter are the natural anchor points for swapping each partition's `source` step from `Csv.Document(File.Contents(ProjectRoot & ...))` to a `Lakehouse.Contents(...)` / `Fabric.Warehouse(...)` query — but that's a semantic-model change outside the scope of a documentation update, and hasn't been done.

**To open and refresh this project on your own machine:** set the `ProjectRoot` parameter (Transform data → Manage Parameters, or edit `model.tmdl` directly) to the absolute path of your local clone of this repository, then Refresh.

### Fact tables

- `FactEnrollment` — one row per student registration in one section for one academic term.
- `RecruitmentFunnel` — one row per application with admission and deposit outcomes.
- `CensusEnrollment` — one row per student-term census record.

### Dimension tables

- `dim_school` — school names and codes used by slicers and chart axes.
- `dim_program` — program names, degree levels, and CIP codes used by slicers and analysis.
- `dim_term` — academic term names, academic years, and dates used by slicers and time analysis.

The fact and dimension tables are related through their documented keys: `school_id`, `program_id`, and `term_id`. The semantic model uses active, single-direction, many-to-one relationships from each fact table to the corresponding dimension table.

### Governance/reference tables

The Institutional Data Trust and Data Lineage & Certification pages import these tables:

- `certification_catalog`
- `lineage_summary`
- `quality_test_evidence`

These tables are generated from the certification catalog, lineage documentation, and actual dbt test results — governance evidence, not illustrative sample data.

To refresh the source CSVs after re-running `dbt build`:

```bash
POSTGRES_PORT=55432 bash scripts/export_mart_csvs.sh
python3 scripts/export_dashboard_reference_csvs.py
python3 scripts/export_onelake_dimension_tables.py
```

`scripts/export_dashboard_reference_csvs.py` regenerates `certification_catalog.csv`, `lineage_summary.csv`, and `quality_test_evidence.csv` from `certification/catalog.yml`, `docs/phase4/lineage.md`, and `target/run_results.json`. After running these, Refresh the semantic model in Power BI Desktop (or re-open the project) to pick up the changes — no Lakehouse upload step is needed given the current local-CSV import.

## Governed metrics

The model's DAX measures (`Enrolled`, `Applications`, `Admits`, `Deposits`, `Yield`, `CensusEnrollment`, `IpedsEnrollment`) are written to match `semantic/metric_definitions.yml`'s `calculation` field for each metric exactly — not approximated with unfiltered row counts.

## Remaining manual Power BI Desktop step

The three report pages (`Executive Enrollment & Admissions`, `Institutional Data Trust`, `Data Lineage & Certification`) exist and are navigable, but none of their visuals (cards, charts, tables, slicers) have been placed yet. See **`PowerBIVisualizationInstructions.md`** (repository root) for the exact field-by-field, page-by-page checklist — it covers every visual called for in each `report-spec.yml`, flags the two places the visuals need a small judgment call rather than a literal spec reading (the funnel on page 1, the non-existent `release_gate` field on page 2), and explains how to save the finished project back out as a `.pbix`. Validate the finished pages against the Phase 3 dbt marts and Phase 4 certification catalog before presenting.
