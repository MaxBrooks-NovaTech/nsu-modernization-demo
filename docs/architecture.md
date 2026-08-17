# Architecture

## Purpose

This repository is a demonstration of a governed institutional BI data-product operating model. It is isolated, synthetic, and not an NSU production implementation.

## End-to-end flow

```text
Synthetic source-style extracts
  -> PostgreSQL raw schema (Docker)
  -> dbt staging views
  -> dbt intermediate registration context
  -> certified analytical marts
  -> governed semantic definitions and data contract
  -> quality gates, lineage, and certification catalog
  -> Power BI/PBIP report specifications
  -> institutional decision support
```

## Current-state narrative

SQL Server/Banner represents the conceptual source environment in the project's narrative, with Evisions Argos (or an equivalent ad-hoc reporting tool) as the conceptual stand-in for the disconnected, self-service reporting layer that typically grows up around Banner — many offices, many canned reports, no shared semantic layer. `docs/legacy-reporting/` makes that concrete with four real, differently-defined "enrollment" numbers computed against this demo's own data. The runnable demonstration uses local PostgreSQL in Docker and never connects to NSU systems. This separation demonstrates modernization without breaking existing systems or exposing production student data.

## Certified products

- `analytics.fact_enrollment`: registration grain; one row per student registration in one section for one academic term.
- `analytics.fact_recruitment_funnel`: one row per application with admissions and deposit outcomes.
- `analytics.fact_census_enrollment`: one row per student-term census record.

## Governance controls

- Deterministic synthetic generation and reset lifecycle.
- Database keys and relationship tests prevent accidental fan-out.
- dbt tests and source freshness checks provide release evidence.
- `contracts/fact_enrollment.yml` defines the principal contract.
- `certification/catalog.yml` records approval and consumer impact.
- `docs/phase4/lineage.md` documents source-to-report impact paths.
- `docs/data-dictionary.md` documents certified mart columns, grain, sources, and quality coverage.
- `scripts/check_contract_changes.py` detects breaking contract and certified-metric changes.
- `docs/ferpa-ipeds-governance.md` maps existing controls (sensitivity classification, lineage, grain, change detection) to FERPA/IPEDS requirements.

## Boundaries

The demonstration does not provide live Banner, SQL Server, Fabric, Purview, enterprise authentication, or native Power BI Desktop output on macOS. These are documented as conceptual or manual integration points rather than claimed artifacts.
