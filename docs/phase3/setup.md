# Phase 3 — Semantic Layer, Data Contracts & Data Quality

Phase 3 establishes institutional data governance, certified semantic metric definitions, actionable data contracts, and an automated data quality test harness across the NSU demonstration platform.

## Purpose & Scope

Phase 3 transitions the project from a raw transformation pipeline to a governed institutional data product architecture:

1. **Governed Semantic Layer**: Formalizes 7 certified institutional metrics with standard calculations, grains, ownership, and stewards.
2. **Actionable Data Contracts**: Establishes machine-readable contract specifications for core facts (`analytics.fact_enrollment`) with freshness SLAs, schema enforcement, and breaking change rules.
3. **Certified Marts Expansion**: Delivers dedicated marts for recruitment funnel analysis (`fact_recruitment_funnel`) and official census reporting (`fact_census_enrollment`).
4. **Data Quality Suite**: Implements 46 automated tests covering schema integrity, referential relationships, uniqueness, and business logic.

---

## Governed Semantic Metrics

Defined in `semantic/metric_definitions.yml`:

| Metric                | Grain                            | Calculation / Source                                                | Owner / Steward                               |
| --------------------- | -------------------------------- | ------------------------------------------------------------------- | --------------------------------------------- |
| **Applications**      | `application_id`                 | Submitted applications in `analytics.fact_recruitment_funnel`       | Institutional Research / Data Governance Lead |
| **Admits**            | `application_id`                 | Admitted applicants in `analytics.fact_recruitment_funnel`          | Institutional Research / Data Governance Lead |
| **Deposits**          | `deposit_id`                     | Paid deposits in `analytics.fact_recruitment_funnel`                | Institutional Research / Data Governance Lead |
| **Enrolled**          | `registration_id`                | Active registrations (`Registered`) in `analytics.fact_enrollment`   | Institutional Research / Data Governance Lead |
| **Yield**             | `term_id, school_id, program_id` | `Deposits / Admits` conversion ratio                                | Institutional Research / Data Governance Lead |
| **Census Enrollment** | `student_id, term_id`            | Census-date enrolled students in `analytics.fact_census_enrollment` | Institutional Research / Data Governance Lead |
| **IPEDS Enrollment**  | `student_id, term_id`            | IPEDS-eligible student cohort in `analytics.fact_census_enrollment` | Institutional Research / Data Governance Lead |

### Resolving Conflicting Numbers

The semantic layer explicitly disambiguates common higher-education metric discrepancies:

- **Course Registration Volume** (1,897 active registrations) vs.
- **Census Headcount** (240 unique students / 1,072 enrolled student-terms) vs.
- **Recruitment Funnel Cohorts** (300 applications / 201 admits / 109 paid deposits).

---

## Data Contracts

Defined in `contracts/fact_enrollment.yml`:

- **Model**: `analytics.fact_enrollment` (v1.0.0, Certified)
- **Grain**: One row per student registration in one section for one academic term.
- **Freshness SLA**: 24-hour target.
- **Required Fields**: `registration_id`, `student_id`, `section_id`, `term_id`, `registration_status`, `credit_hours`.
- **Breaking Change Policies**: Major version bump required for field removal/renaming, grain alterations, or formula revisions. Additive nullable fields are minor-version changes.

---

## Certified Mart Models

1. **`analytics.fact_enrollment`** (2,148 rows):
   - One row per registration event.
   - Preserves complete course-section and registration context.
2. **`analytics.fact_recruitment_funnel`** (300 rows):
   - One row per submitted application with left-joined admission and deposit milestones.
   - Contains boolean flags `is_admitted` and `is_deposited`.
3. **`analytics.fact_census_enrollment`** (1,074 rows):
   - One row per student-term census record.
   - Contains boolean flags `census_enrolled_flag` and `ipeds_enrolled_flag`, plus total term credit hours.

---

## Automated Data Quality Suite

Phase 3 executes 46 automated data tests:

- **Nullability & Uniqueness**: Primary keys validated across all 11 `raw` sources, staging views, and mart tables.
- **Referential Integrity**: Relationship tests linking marts and staging entities back to dimensional sources (`schools`, `programs`, `terms`, `students`, `course_sections`).
- **Singular Grain Tests**:
  - `tests/fact_enrollment_grain.sql`: Verifies composite uniqueness on `(student_id, section_id, term_id)`.
  - `tests/fact_census_enrollment_grain.sql`: Verifies uniqueness on `(student_id, term_id)`.
- **Business Rule Invariants**:
  - `tests/fact_enrollment_business_rules.sql`: Enforces positive credit hours on active registrations and zero credit hours on dropped courses.

---

## How to Run & Verify Phase 3

```bash
# Ensure PostgreSQL container is running
POSTGRES_PORT=55432 docker compose up -d

# Build all views, marts, and execute all 46 data tests
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password \
  .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors
```
