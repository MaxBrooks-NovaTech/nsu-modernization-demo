# Phase 4 — Lineage

## Purpose

This document records the demonstrable source-to-consumption lineage for the synthetic NSU BI interview demonstration. The PostgreSQL database is local demonstration infrastructure, not NSU production.

## End-to-end lineage

```text
Conceptual Banner / SQL Server source
  -> raw.* PostgreSQL landing tables (synthetic seed data)
  -> staging.* dbt views
  -> intermediate.int_registration_context
  -> analytics.FactEnrollment
  -> semantic/metric_definitions.yml
  -> Power BI / downstream data products (planned Phase 5 artifacts)
```

## Certified product lineage

| Product                             | Source entities                                                                                        | Transformations                                                                                  | Semantic definitions                  | Consumers                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------- | ----------------------------------------------------------------------------- |
| `analytics.FactEnrollment`          | `raw.registrations`, `raw.course_sections`, `raw.students`, `raw.terms`, `raw.schools`, `raw.programs` | `stg_*` views; `int_registration_context`; `models/marts/fact_enrollment.sql`                    | Enrolled                              | Executive Enrollment and Admissions reporting; downstream enrollment analysis |
| `analytics.fact_recruitment_funnel` | `raw.applications`, `raw.admissions`, `raw.deposits`                                                   | `stg_applications`, `stg_admissions`, `stg_deposits`; `models/marts/fact_recruitment_funnel.sql` | Applications, Admits, Deposits, Yield | Admissions funnel reporting                                                   |
| `analytics.fact_census_enrollment`  | `raw.enrollment_census`, `raw.students`, `raw.terms`, `raw.schools`, `raw.programs`                    | `stg_enrollment_census`; `models/marts/fact_census_enrollment.sql`                               | Census Enrollment, IPEDS Enrollment   | Official census and institutional reporting                                   |

## Impact analysis

A source schema or grain change is assessed through `scripts/check_contract_changes.py` against `contracts/fact_enrollment.yml`. The certification catalog identifies affected semantic definitions and consumers so a change can be blocked or routed for re-certification before release.

## Limitations

This is a source-controlled demonstration lineage map. It does not claim live SQL Server, Banner, Fabric, Purview, or Power BI metadata integration.

