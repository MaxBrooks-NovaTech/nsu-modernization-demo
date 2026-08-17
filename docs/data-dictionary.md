# Data Dictionary

Column-level reference for the three certified analytical marts in `analytics`. Governed business definitions for the metrics built on top of these marts live in `semantic/metric_definitions.yml`; this document covers the underlying fields, not the metrics themselves. See `docs/architecture.md` for how these marts fit into the end-to-end flow, `docs/phase4/lineage.md` for source-to-report lineage, and `docs/er_diagrams/` for visual ER diagrams of both the transactional and analytics schemas.

## `analytics.fact_enrollment`

**Grain**: one row = one student registration in one section for one academic term. Certified via `contracts/fact_enrollment.yml`.

| Column | Type | Source | Description |
| --- | --- | --- | --- |
| `registration_id` | text (PK) | `raw.registrations` | Unique identifier for one student's registration in one section/term. Grain key. |
| `student_id` | text | `raw.registrations` | Registering student. References `raw.students`. |
| `section_id` | text | `raw.registrations` | Course section registered into. References `raw.course_sections`. |
| `term_id` | text | `raw.registrations` | Academic term of the registration. References `raw.terms`. |
| `school_id` | text | `raw.course_sections` | School offering the section (not necessarily the student's admitting school). |
| `program_id` | text | `raw.course_sections` | Program offering the section. |
| `course_code` | text | `raw.course_sections` | Course identifier (e.g. subject + number). |
| `section_number` | text | `raw.course_sections` | Section number within the course/term. |
| `registration_date` | date | `raw.registrations` | Date the registration was recorded. |
| `registration_status` | text | `raw.registrations` | One of `Registered`, `Dropped`, `Withdrawn`. Enforced by `accepted_values` test. |
| `credit_hours` | numeric(4,1) | `raw.registrations` | Credit hours for the registration. `0` only permitted when `registration_status = Dropped`; must be `> 0` for `Registered`/`Withdrawn` (`fact_enrollment_business_rules` test). |
| `grade_mode` | text | `raw.registrations` | Grading basis for the registration. |
| `student_type` | text | `raw.students` | Student classification at the student level (e.g. new, continuing, transfer). |
| `residency_status` | text | `raw.students` | Student's residency classification. |
| `admit_school_id` | text | `raw.students` | School the student was originally admitted to (may differ from the section's `school_id`). |
| `admit_program_id` | text | `raw.students` | Program the student was originally admitted to. |
| `modality` | text | `raw.course_sections` | Delivery mode of the section (e.g. in-person, online, hybrid). |
| `capacity` | integer | `raw.course_sections` | Maximum enrollment capacity of the section. |

**Tests**: `not_null`, `unique`, `accepted_values`, `relationships` (to `stg_students`, `stg_course_sections`, `stg_terms`), custom composite-grain test (`tests/fact_enrollment_grain.sql`), business-rule test (`tests/fact_enrollment_business_rules.sql`), minimum-row-count test (`tests/fact_enrollment_minimum_row_count.sql`). Freshness enforced via `models/staging/sources.yml` (`warn_after: 18h`, `error_after: 24h`) against `loaded_at` on all contributing `raw.*` sources.

## `analytics.fact_recruitment_funnel`

**Grain**: one row = one application, with its admission and deposit outcome if any.

| Column | Type | Source | Description |
|---|---|---|---|
| `application_id` | text (PK) | `raw.applications` | Unique application identifier. Grain key. |
| `student_id` | text | `raw.applications` | Applicant. References `raw.students`. |
| `term_id` | text | `raw.applications` | Term the application targets. |
| `school_id` | text | `raw.applications` | School applied to. |
| `program_id` | text | `raw.applications` | Program applied to. |
| `application_date` | date | `raw.applications` | Date the application was submitted. |
| `application_status` | text | `raw.applications` | Status of the application (e.g. `Submitted`). Drives the `applications` metric. |
| `admission_id` | text, nullable | `raw.admissions` | Admission record, if a decision has been made. `null` for applications with no decision yet. |
| `decision_date` | date, nullable | `raw.admissions` | Date of the admission decision. |
| `decision_status` | text, nullable | `raw.admissions` | Admission decision (e.g. `Admitted`). Drives the `admits` metric. |
| `deposit_id` | text, nullable | `raw.deposits` | Deposit record, if the admitted student made one. |
| `deposit_date` | date, nullable | `raw.deposits` | Date the deposit was recorded. |
| `deposit_status` | text, nullable | `raw.deposits` | Deposit status (e.g. `Paid`). Drives the `deposits` metric. |
| `deposit_amount` | numeric(10,2), nullable | `raw.deposits` | Deposit amount. |
| `is_admitted` | boolean | derived | `true` when `admission_id is not null`. |
| `is_deposited` | boolean | derived | `true` when `deposit_id is not null and deposit_status = 'Paid'`. |

**Tests**: `not_null`/`unique` on `application_id`, `not_null` on `student_id`/`term_id`/`application_status`, `relationships` to `stg_students`/`stg_terms`. Grain integrity relies on `raw.admissions.application_id` and `raw.deposits.admission_id` both being database-level `UNIQUE`, so the left joins that build this mart cannot fan out.

## `analytics.fact_census_enrollment`

**Grain**: one row = one student per academic term, as of the institutional census date.

| Column | Type | Source | Description |
|---|---|---|---|
| `enrollment_id` | text (PK) | `raw.enrollment_census` | Unique census record identifier. |
| `student_id` | text | `raw.enrollment_census` | Student. Grain key (with `term_id`). |
| `term_id` | text | `raw.enrollment_census` | Academic term. Grain key (with `student_id`). |
| `school_id` | text | `raw.enrollment_census` | Student's school as of census. |
| `program_id` | text | `raw.enrollment_census` | Student's program as of census. |
| `census_enrolled_flag` | boolean | `raw.enrollment_census` | `true` if the student counts as enrolled at the institutional census date. Drives the `census_enrollment` metric. |
| `ipeds_enrolled_flag` | boolean | `raw.enrollment_census` | `true` if the student meets the synthetic IPEDS enrollment inclusion rule. Drives the `ipeds_enrollment` metric. |
| `total_credit_hours` | numeric(5,1) | `raw.enrollment_census` | Total credit hours for the student in the term as of census. |
| `enrollment_status` | text | `raw.enrollment_census` | Enrollment status label as of census. |

**Tests**: `not_null`/`unique` on `enrollment_id`, `not_null` on `student_id`/`term_id`/`census_enrolled_flag`/`ipeds_enrolled_flag`, custom composite-grain test (`tests/fact_census_enrollment_grain.sql`) enforcing one row per `(student_id, term_id)`.

## Notes

- All `raw.*` source tables carry a `loaded_at timestamptz` column (added for freshness enforcement — see `docs/setup.md`); it is not exposed on the marts above since it is a pipeline-operational field, not a business attribute.
- Full source table definitions (types, keys, foreign keys) are in `db/init/01_schema.sql`. Full test definitions are in `models/marts/schema.yml`, `models/staging/sources.yml`, and `tests/*.sql`.
- This dictionary describes fields, not governed business calculations — for certified metric definitions (Applications, Admits, Deposits, Enrolled, Yield, Census Enrollment, IPEDS Enrollment), see `semantic/metric_definitions.yml`.
