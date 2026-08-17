# FERPA and IPEDS Governance

This project handles synthetic student enrollment and admissions data. The two compliance frameworks that would govern this data if it were real are **FERPA** (student privacy) and **IPEDS** (federal enrollment reporting) — and they pull in opposite directions on the same data, which is exactly why they belong in a governance model together rather than as an afterthought.

## Why synthetic data doesn't make this irrelevant

`scripts/generate_synthetic_data.py` generates deterministic fake students, applications, and registrations — no real NSU student is represented anywhere in this repository (see `AGENTS.md` §8, `CLAUDE.md` §14). That means FERPA doesn't technically apply to *this data*. It doesn't mean FERPA is irrelevant to *this architecture*: the point of the demo is that the governance model (contracts, certification, sensitivity classification, lineage, restricted consumption) is what makes a real deployment FERPA-defensible later. Building that structure in now, against safe synthetic data, is the point — retrofitting privacy controls onto an ungoverned warehouse after the fact is a much harder conversation than designing them in from the start.

## FERPA, briefly

The Family Educational Rights and Privacy Act governs access to a student's **education records** — most of what this project's fact tables model (registrations, admissions, enrollment status) qualifies. In broad terms:

- Personally identifiable education records require a legitimate educational interest to access, or the student's consent.
- **Directory information** (name, enrollment status, dates of attendance) can generally be disclosed unless the student opts out — this demo doesn't model directory-information opt-outs, since there's no real student to opt out.
- **Aggregate, de-identified data** — counts and rates with no individual student identifiable — falls outside FERPA's disclosure restrictions. This is the exception that makes institutional reporting (including IPEDS) possible at all.

## IPEDS, briefly

The Integrated Postsecondary Education Data System is the federal government's mandatory enrollment/completion/finance reporting system for institutions receiving federal student aid. IPEDS reporting is **aggregate by construction** — headcounts and rates by category, not student-level extracts — which is exactly the FERPA aggregate-disclosure exception described above. `ipeds_enrollment` is already one of this project's 7 certified metrics (`semantic/metric_definitions.yml`), built from `analytics.fact_census_enrollment`'s `ipeds_enrolled_flag`.

## Where FERPA and IPEDS meet — and why that's a governance problem, not just a policy one

IPEDS reporting requires pulling from the same student-level education records FERPA restricts, then *aggregating out* the individual before anything leaves the institution. That transformation — student-level records in, de-identified counts out — is a data pipeline problem as much as a compliance one:

- **Wrong grain in, wrong report out.** If the pipeline computing an IPEDS count accidentally operates at the wrong grain (e.g., double-counting a student registered in multiple sections — see `docs/legacy-reporting/README.md` for exactly this failure mode with the Registrar's 376-vs-188 discrepancy), the aggregate submitted to the federal government is wrong, and there's no way to tell from the aggregate alone.
- **No lineage, no defensibility.** If a federal auditor or an internal reviewer asks "how was this IPEDS number derived, and what raw records fed it," an ungoverned report has no answer. `docs/phase4/lineage.md` traces `analytics.fact_census_enrollment` back through `raw.enrollment_census` to `raw.students`/`raw.terms` for exactly this reason.
- **Uncontrolled downstream access defeats the aggregation.** An aggregate IPEDS number is FERPA-safe; the student-level table it was computed from is not. Access to `analytics.fact_census_enrollment` and `analytics.fact_enrollment` (student-level, registration-level) needs to be governed differently than access to a published IPEDS summary — this is what the `sensitivity` field on every metric in `semantic/metric_definitions.yml` exists to signal.

## How this project's existing governance controls map to FERPA/IPEDS needs

Nothing new was built for this — the controls already exist for general data-governance reasons and happen to map directly onto FERPA/IPEDS concerns:

| Existing control | FERPA/IPEDS relevance |
| --- | --- |
| `semantic/metric_definitions.yml`'s `sensitivity` field on every metric (e.g. `census_enrollment`: *"Internal aggregate; restricted student-level access."*; `yield`: *"suppress small groups in consumption"*) | Marks which metrics are safe to disclose as aggregates versus which require restricted, need-to-know access — the FERPA directory-vs-education-record distinction, encoded per metric rather than left to reader judgment. |
| `certification/catalog.yml`'s `owner`/`steward`/`approval` fields | FERPA access decisions require accountability — a named steward per certified product, not an anonymous shared drive. |
| `docs/phase4/lineage.md` (source → transformation → model → semantic definition → report) | Answers "where did this number come from" for any IPEDS submission or ad-hoc report — the defensibility gap described above. |
| `contracts/fact_enrollment.yml`'s explicit grain (`one row = one student registration in one section for one academic term`) and grain tests (`tests/fact_enrollment_grain.sql`) | Prevents the exact double-counting failure mode shown in `docs/legacy-reporting/`, which would otherwise produce a materially wrong federal report. |
| `scripts/check_contract_changes.py`'s certified-metric and grain change detection | Catches a silent redefinition of `ipeds_enrollment`'s calculation before it ships — exactly the kind of change that would make a federal submission wrong without anyone noticing. |
| Small-group suppression note on `yield` | A real FERPA/IPEDS control: aggregates over very small cohorts can still be individually identifying, so cell suppression is a named requirement, not an assumption. |

## Known limitations (be direct about these when presenting this project)

- This demo does not implement row-level or column-level access control — `sensitivity` values are documentation, not an enforced permission system. In a real deployment, `census_enrollment`/`fact_enrollment` (student-level) and `ipeds_enrollment`/aggregate reports would need actual database or BI-tool-level access restrictions layered on top of this same governance metadata.
- No directory-information opt-out modeling, no FERPA consent/disclosure-log tracking, no actual small-cell suppression logic (the `yield` sensitivity note is a documented intent, not a query-level enforcement).
- IPEDS's real submission specifications (exact cohort definitions, reporting windows, survey components) are far more detailed than the single synthetic `ipeds_enrolled_flag` this demo uses — `ipeds_enrollment` here demonstrates the *governance pattern* for a federal aggregate metric, not a production-ready IPEDS submission pipeline.
