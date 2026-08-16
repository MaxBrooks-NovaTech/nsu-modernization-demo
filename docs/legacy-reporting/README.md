# Legacy Reporting — The "Before" Picture

This directory is the counterpart to `semantic/metric_definitions.yml`: four synthetic Argos-style report exports, each claiming to answer the same question — *"How many students are enrolled this Fall?"* — for the same real term (`2025FA`) in this demo's database. None of them was built with a shared, governed definition. All four numbers are real query results against this project's own synthetic data (see `docs/legacy-reporting/README.md#how-these-numbers-were-produced` below) — the discrepancy isn't fabricated, it's what actually happens when four offices independently write four different queries against the same underlying transactional data.

Evisions Argos (or an equivalent ad-hoc reporting tool) is the realistic stand-in here for "whatever canned/self-service reporting tool sits on top of Banner" — the point isn't the specific tool, it's that ungoverned, siloed reports proliferate around a legacy source system with no shared semantic layer.

## The four reports

| File | Office | "Enrolled Students," Fall 2025 | What it's actually counting |
| --- | --- | --- | --- |
| `argos_registrar_fall2025.csv` | Registrar's Office | **376** | Every registration row for the term — includes Dropped and Withdrawn, and double-counts students registered in multiple sections. This is a *registration-event* count, not a student count. |
| `argos_enrollment_management_fall2025.csv` | Enrollment Management | **188** | Distinct students with any registration row this term, regardless of status — includes students who later dropped every section. |
| `argos_finance_fall2025.csv` | Finance / Billing | **188** | Distinct students with `credit_hours > 0` — coincidentally the same number this term, but for a different reason (it happens to include Withdrawn students as still "billable," which Enrollment Management's report does not intend to). |
| `argos_census_office_fall2025.csv` | Institutional Research | **188** | An official census-date snapshot — the most rigorous of the four, but its methodology lives in a separate memo, not attached to the report, and isn't shared with the other three offices. |

None of the four report exports document their filter logic in a way another office could check against. `definition_documented` is `No` on three of them, and "partially, in a separate memo" on the fourth.

## The certified answer

`semantic/metric_definitions.yml`'s `enrolled` metric, applied to the same term:

```text
count_distinct(registration_id) where registration_status = Registered   →   336
```

**336** — not 376, not 188. It's a fifth number, and it's the correct one for the question "how many active registrations does Fall 2025 have," because it's the only one of the five that matches the contract's actual grain (`contracts/fact_enrollment.yml`: one row = one student registration in one section for one academic term) with the actual governed status filter, both fully documented and both testable (`tests/fact_enrollment_grain.sql`, `tests/fact_enrollment_business_rules.sql`).

The lesson isn't "336 is bigger/better than 188" — it's that **376, 188, 188, and 188 are four different, real numbers produced by four reasonable-sounding but undocumented and mutually inconsistent queries**, and none of the four report owners could tell you why their number differs from the others' without reverse-engineering someone else's Argos report. `docs/images/legacy-vs-certified-enrollment.png` visualizes this contrast.

## How these numbers were produced

Not invented — computed directly against this project's real synthetic `raw.registrations` and `raw.enrollment_census` tables for `term_id = '2025FA'`:

```sql
-- Registrar (376): every registration row, any status
select count(*) from raw.registrations where term_id = '2025FA';

-- Enrollment Management (188): distinct students, any status
select count(distinct student_id) from raw.registrations where term_id = '2025FA';

-- Finance (188): distinct students with billable credit hours
select count(distinct student_id) from raw.registrations where term_id = '2025FA' and credit_hours > 0;

-- Institutional Research / census (188): official census-date snapshot
select count(distinct student_id) from raw.enrollment_census where term_id = '2025FA' and census_enrolled_flag = true;

-- Certified (336): the governed "enrolled" definition
select count(distinct registration_id) from raw.registrations where term_id = '2025FA' and registration_status = 'Registered';
```

## Using this in the demo

`docs/demo.md` step 1 ("many reports, many definitions, uneven trust") can open one or two of these CSVs to make that abstract claim concrete before showing the certified alternative — see `docs/images/legacy-vs-certified-enrollment.png` for a ready-made visual.
