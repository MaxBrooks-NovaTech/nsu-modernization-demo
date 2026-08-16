# Phase 5 — Power BI / PBIP
This directory contains source-controlled Power BI project specifications for the interview demonstration. Power BI Desktop is not available in the current macOS environment, so these files document the intended PBIP model, report pages, fields, measures, and governance metadata without claiming that a `.pbix` file or rendered screenshots exist.

## Reports
1. `executive-enrollment-admissions/` — Executive Enrollment & Admissions
2. `institutional-data-trust/` — Institutional Data Trust
3. `data-lineage-certification/` — Data Lineage & Certification
Each report specification points to the certified PostgreSQL marts and references the semantic definitions and certification catalog. The model is intentionally synthetic and local.

## Manual Power BI Desktop step
The manual Power BI Desktop step is required to produce a native PBIP project on Windows.
On Windows with Power BI Desktop, create a PBIP project using the supplied specification, connect to the local PostgreSQL database, create the listed measures/pages, and save the project in PBIP format. Validate the three pages against the Phase 3 dbt marts and Phase 4 certification catalog before presenting.
