# codex-handoff.md

# Codex -> Claude Handoff
## Phase
PHASE 6
## Status
IMPLEMENTED AND VALIDATED — READY FOR CLAUDE REVIEW; PAUSED BEFORE PHASE 7

## Objective
Implement and validate Phase 6 architecture, setup, and interview demonstration documentation without expanding into Phase 7 final QA or changing certified models and metrics.

---

## Implemented
- Added `docs/architecture.md` describing the actual source-to-consumption architecture, certified products, governance controls, and boundaries.
- Added `docs/setup.md` with reproducible Docker, synthetic-data, source-freshness, dbt build, port override, and safety instructions.
- Added `docs/demo.md` with an interview-ready walkthrough, commands, talking points, and known limitations.
- Updated the root README with links to Phase 6 documentation, lineage, certification, Power BI specifications, and Gemini review.
- Validated all documentation artifacts and required README links.
- Confirmed Gemini Phase 4 review verdict: PASS with 0 P0 and 0 P1 issues; one P2 suggestion was approved for Phase 5 handling.
- Commenced Phase 5 under explicit human authorization.
- Added `powerbi/README.md` documenting the PBIP specifications, report targets, and unavoidable Power BI Desktop manual step.
- Added source-controlled report specifications for Executive Enrollment & Admissions, Institutional Data Trust, and Data Lineage & Certification.
- Connected the specifications to certified marts, semantic definitions, lineage, and certification metadata.
- Human approved proceeding after Gemini returned Phase 3 PASS with only P2 suggestions.
- Added `docs/phase4/lineage.md` with source-to-transformation-to-model-to-semantic-to-consumer lineage and impact analysis.
- Added `certification/catalog.yml` with owner, steward, definitions, tests, lineage, approval, status, version, and consumers for three certified products.
- Added `scripts/check_contract_changes.py` to detect required-field removal, grain changes, and contract governance-rule changes.
- Verified unchanged contracts pass change detection without false positives.

- Verified existing remote origin:
  `https://github.com/MaxBrooks-NovaTech/nsu-modernization-demo.git`
- Reviewed and followed the Gemini-authoritative project documents:
  `docs/CODEX_IMPLEMENTATION_SPEC_GEMINI.md`,
  `AGENTS_WITH_GEMINI.md`,
  `docs/implementation-status-gemini.md`,
  `docs/CODEX_IMPLEMENTATION_SPEC.md`,
  `docs/implementation-status.md`,
  `docs/handoff/codex-handoff.md`, and
  `docs/handoff/claude-review.md`
- Created README.md for private repository publication.
- Expanded README.md into a full finished-project style overview with quick
  start, architecture, data model, semantic definitions, quality, contracts,
  lineage, certification, Power BI, and demo walkthrough sections.
- Populated .env.example with placeholder-only values for expected local and
  optional integration secrets.
- Enabled VS Code Python terminal env-file loading.
- Aligned Gemini-specific Codex and review instruction documents to reference
  the Gemini implementation spec, Gemini status file, and Gemini review handoff.
- Updated .env.example placeholders to match the project-standard hyphenated key
  naming convention.
- Completed Phase 0 repository audit.
- Confirmed Claude is the primary reviewer for this handoff.
- Documented Gemini as fallback only if Claude returns an availability, usage,
  or credit error.
- Activated Gemini fallback after Claude session limit was reached.
- Fixed Gemini P1 findings:
  - removed `.DS_Store` from Git tracking while preserving the local file;
  - expanded `.gitignore` for OS, Python, dbt, logs, caches, and local env
    artifacts;
  - normalized `.env.example` keys to uppercase underscore names;
  - synchronized Gemini and main status files.
- Implemented Phase 1 Docker Compose PostgreSQL 16 foundation.
- Implemented deterministic synthetic data generation with all required source-style tables and all 12 schools.
- Implemented PostgreSQL schema/load initialization, reset, validation, and setup documentation.
- Verified the running database with Docker Desktop using host port `55432` because `5432` was unavailable.
- Implemented Gemini Phase 1 review fixes: `students.entry_term_id` foreign key, dependency-correct seed load order, exact row-count and complete reviewed FK assertions, budget and section business uniqueness constraints, and port-collision setup documentation.
- Began human-authorized Phase 2 without changing the approved FactEnrollment grain.
- Added dbt project/profile configuration using dbt-core 1.10.13 and dbt-postgres 1.9.0.
- Added raw source declarations, six staging models, an intermediate registration context, and `analytics.FactEnrollment`.
- Added model tests for nulls, uniqueness, accepted registration statuses, and the custom `(student_id, section_id, term_id)` grain.
- Added staging models for applications, admissions, deposits, census enrollment, and budget actuals.
- Added certified recruitment funnel and census enrollment marts.
- Added semantic definitions for Applications, Admits, Deposits, Enrolled, Yield, Census Enrollment, and IPEDS Enrollment.
- Added `contracts/fact_enrollment.yml` with schema, grain, freshness, quality, ownership, versioning, and breaking-change rules.
- Added source/model relationships, census grain, and enrollment business-rule tests.

---

## Files Changed
- docs/implementation-status.md
- docs/handoff/codex-handoff.md
- .vscode/settings.json
- requirements.txt
- docker-compose.yml
- db/init/01_schema.sql
- db/init/02_load_seed_data.sql
- scripts/generate_synthetic_data.py
- scripts/reset_phase1.sh
- scripts/validate_phase1.sh
- seeds/*.csv
- docs/phase1/setup.md
- dbt_project.yml
- profiles.yml.example
- models/staging/*.sql
- models/staging/sources.yml
- models/intermediate/int_registration_context.sql
- models/marts/fact_enrollment.sql
- models/marts/schema.yml
- tests/fact_enrollment_grain.sql
- macros/generate_schema_name.sql
- docs/phase2/setup.md
- semantic/metric_definitions.yml
- contracts/fact_enrollment.yml
- models/staging/stg_applications.sql
- models/staging/stg_admissions.sql
- models/staging/stg_deposits.sql
- models/staging/stg_enrollment_census.sql
- models/staging/stg_budget_actuals.sql
- models/marts/fact_recruitment_funnel.sql
- models/marts/fact_census_enrollment.sql
- tests/fact_enrollment_business_rules.sql
- tests/fact_census_enrollment_grain.sql
- requirements.txt
- .gitignore
- Previously changed Phase 0 files remain in the repository history.

---

## Commands Executed

- `git status --short --branch`
- `rg --files`
- `git remote -v`
- `sed -n '1,260p' docs/CODEX_IMPLEMENTATION_SPEC.md`
- `sed -n '1,240p' docs/implementation-status.md`
- `sed -n '1,240p' docs/handoff/codex-handoff.md`
- `sed -n '1,260p' docs/handoff/claude-review.md`
- `date '+%Y-%m-%d %H:%M:%S %Z'`
- `sed -n '1,260p' README.md`
- `sed -n '1,180p' docs/implementation-status.md`
- `sed -n '1,180p' docs/handoff/codex-handoff.md`
- `awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/ {print $1}' .env`
- `sed -n '1,220p' .env.example`
- `sed -n '1,220p' .gitignore`
- `rg -n "OPENAI|ANTHROPIC|CLAUDE|API_KEY|TOKEN|SECRET|PASSWORD|DB_|POSTGRES|DATABASE|ENV" -S .`
- `find . -maxdepth 3 -type f -name '*settings*.json' -o -path './.vscode/*'`
- `rg -n "CLAUDE|Claude|claude|GEMINI|Gemini|gemini|CODEX_IMPLEMENTATION_SPEC|REVIEW_SPEC|implementation-status|handoff" AGENTS.md AGENTS_WITH_GEMINI.md CLAUDE.md GEMINI.md docs max_instructions.md vs_code_instructions.md README.md`
- `rg -n "claude-review|CLAUDE_REVIEW|CLAUDE|Claude|claude|GEMINI-review|CODEX_IMPLEMENTATION_SPEC.md|implementation-status.md" GEMINI.md AGENTS_WITH_GEMINI.md docs/GEMINI_REVIEW_SPEC.md docs/handoff/gemini-review.md docs/CODEX_IMPLEMENTATION_SPEC_GEMINI.md docs/implementation-status-gemini.md`
- `git check-ignore -v .env`
- `git ls-files`
- `git ls-files | rg -n "(^|/)\\.env$|secret|credential|token|key|password|\\.pem$|\\.p12$|\\.pfx$" -i`
- `rg -n "sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{20,}|password\\s*=\\s*[^\\s#]+|client-secret\\s*=\\s*[^\\s#]+|api-key\\s*=\\s*[^\\s#]+|BEGIN (RSA|OPENSSH|PRIVATE) KEY" -S -g '!venv/**' -g '!.git/**' -g '!.env' .`
- artifact existence check for README-claimed implementation paths:
  `docker-compose.yml`, `dbt_project.yml`, `seeds`, `scripts`, `models`,
  `tests`, `semantic`, `contracts`, `lineage`, `certification`, and `powerbi`
- `git rm --cached .DS_Store`
- `sed -n '1,240p' .gitignore`
- `sed -n '1,260p' .env.example`
- `git ls-files .DS_Store .gitignore .env.example docs/implementation-status.md docs/implementation-status-gemini.md docs/handoff/codex-handoff.md docs/handoff/gemini-review.md`

---

## Tests Executed
- `python3 scripts/generate_synthetic_data.py`
- `docker compose config`
- `POSTGRES_PORT=55432 docker compose up -d`
- PostgreSQL readiness check with `pg_isready`
- `psql` raw-schema inspection
- `POSTGRES_PORT=55432 bash scripts/validate_phase1.sh`
- `POSTGRES_PORT=55432 docker compose exec -T postgres psql ...` constraint inspection
- `python3 -m venv .venv`
- `.venv/bin/pip install -r requirements.txt`
- `.venv/bin/dbt debug --project-dir . --profiles-dir .`
- `.venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors` (with `POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password`)

Gemini Phase 1 review fix verification executed:

- `POSTGRES_PORT=55432 bash scripts/reset_phase1.sh` (passed)
- `POSTGRES_PORT=55432 bash scripts/validate_phase1.sh` (passed exact row counts and reviewed FK/grain assertions)
- PostgreSQL catalog inspection confirmed `students_entry_term_id_fkey`, section uniqueness, and budget uniqueness constraints.
- dbt debug passed against the local PostgreSQL container on port `55432`.
- dbt build passed: 16 total results, 0 errors, including 2,148-row `analytics.FactEnrollment` and the custom composite-grain test. dbt seed execution is disabled because the Phase 1 initialization already loads the authoritative `raw` schema.

P1 fix verification executed:

- Confirm `.DS_Store` is no longer tracked.
- Confirm `.DS_Store`, `.env`, Python caches, dbt artifacts, logs, and test
  caches are ignored.
- Confirm `.env.example` keys use uppercase underscore names.
- Confirm no tracked real secrets were introduced.

---

## Actual Results
- Deterministic generation completed with seed `20260816`.
- Generated counts: 12 schools, 36 programs, 240 students, 6 terms, 432 sections, 300 applications, 201 admissions, 109 deposits, 2,148 registrations, 1,074 enrollment census rows, and 24 budget rows.
- PostgreSQL initialized `raw` schema and loaded all 11 tables.
- Validation passed expected row counts, all 12-school requirement, referential-integrity checks, and duplicate registration-grain check.
- Local port `5432` was unavailable; the successful validation used host port `55432` through the existing compose variable.
- Remote origin is already configured for the intended private GitHub repository.
- README.md now reads as a full finished-project repository overview suitable
  for private publication.
- .env.example now contains safe placeholders only; no real .env values were
  copied.
- `.vscode/settings.json` enables `python.terminal.useEnvFile`.
- Gemini-specific instruction docs now reference the correct Gemini document
  names.
- `git status --short --branch` reported `## main...origin/main`.
- `git remote -v` reported the expected private GitHub origin for fetch and
  push.
- `git check-ignore -v .env` confirmed `.env` is ignored by `.gitignore`.
- Secret-pattern scans did not identify tracked real API keys, PATs, private
  keys, or production credentials.
- README.md describes the finished target state; the implementation artifacts it
  names are not present yet.
- Gemini completed Phase 0 review with PASS WITH CONDITIONS.
- All Gemini P0/P1/P2 findings have been addressed by Codex; no P0/P1/P2 findings remain for Phase 1.
- Phase 2 dbt and FactEnrollment implementation passed Gemini review.
- Phase 3 implementation is complete and ready for Gemini review.
- `git ls-files .DS_Store` returned no tracked file.
- `git check-ignore -v` confirmed ignores for `.env`, `.DS_Store`, `target/`,
  `dbt_packages/`, `logs/`, `.pytest_cache/`, and Python cache files.
- `.env.example` key validation found no nonconforming variable names.
- Secret-pattern scan returned no matches.

---

## Known Issues
- Docker Desktop's credential helper was not on the shell `PATH`; validation used `/Applications/Docker.app/Contents/Resources` in `PATH` without changing user configuration.
- The default host port `5432` is occupied on this machine; use the documented `POSTGRES_PORT=55432` override locally when needed.
- Power BI Desktop is unavailable on this macOS environment; actual `.pbip`, `.pbix`, and rendered screenshot generation remains a documented manual step.
- No Power BI artifact is claimed beyond the checked-in specifications.

---

## Blockers
None for the Phase 5 specification implementation. Claude review is complete and P1-3 freshness enforcement is resolved and re-verified.

---

## Decisions Needed
Human should inspect and commit the current changes. Do not begin Phase 6 until explicit Phase 6 authorization is given.

---

## Gemini Review Follow-up
The complete Gemini Phase 1 review is recorded in `docs/handoff/gemini-review.md`. All identified P1 and P2 fixes have been implemented and verified. No P0, P1, or P2 findings remain for Phase 1.

Verification included:

- `raw.students.entry_term_id` foreign-key enforcement;
- dependency-correct seed loading;
- exact row-count assertions for all 11 tables;
- admissions, deposits, students, programs, and enrollment referential-integrity assertions;
- registration-grain duplicate detection;
- budget and course-section business uniqueness constraints;
- documented host-port collision handling.

---

## Claude Review Follow-up
Claude independently reviewed Phases 3–5 on 2026-08-16 (full report: `docs/handoff/claude-review.md`). Verdict: **READY WITH CONDITIONS** (0 P0, 3 P1, 4 P2).

Claude independently re-verified the Gemini Phase 4 `dbt build` claim (61/61 nodes) and confirmed the three `powerbi/*/report-spec.yml` files correctly reference the Phase 3 marts and Phase 4 certification/lineage metadata, with no fabricated `.pbip`/`.pbix`/screenshot artifacts.

Claude found and fixed, in-session, two P1 gaps within existing spec/fix authority (re-verified via `dbt build` and a 12-scenario test suite — see `docs/handoff/claude-review.md`):
1. `scripts/check_contract_changes.py` could not detect changes to certified-metric calculations or certification-status downgrades (it never inspected `semantic/metric_definitions.yml`). Added `compare_metrics()` and a top-level status-downgrade check.
2. The contract's `minimum_row_count: 1` was unenforced metadata. Added `tests/fact_enrollment_minimum_row_count.sql`, wired it into `contracts/fact_enrollment.yml` and `certification/catalog.yml`.

**P1-1 — RESOLVED 2026-08-16.** The human confirmed that Phase 4/5 authorization is recorded in the human's own git commits: `da65f14` ("Phase 4 build and review + human approval complete") and `ab12374` ("Claude has entered the chat for review of phase 5. Codex completed build for it"), both authored and committed personally by `MaxBrooks-BI <brooks.maxj@gmail.com>` on 2026-08-16. No further action needed.

**P1-3 — RESOLVED 2026-08-16.** Added `loaded_at` columns to all 11 raw tables, explicit seed-load column lists, and dbt source freshness thresholds. Reset/load passed, 11/11 freshness checks passed, and full dbt build passed 62/62 with 0 errors and 0 warnings.

---

## Revised Instructions for Codex

Human authorization for Phase 4 and Phase 5 is confirmed (commits `da65f14`, `ab12374`). Do **not** re-raise or re-litigate P1-1. The single remaining item before Phase 6 is **P1-3 (freshness enforcement)**. Pick one of the two options below — either is acceptable to Claude — implement it, then hand back for a short re-check. Do not begin Phase 6 work in the same pass; stop after this item and update the status docs.

### Option A — Implement a real freshness check (preferred if time allows)
1. Add a `loaded_at timestamptz not null default now()` column to each `raw.*` table in `db/init/01_schema.sql` (or a single shared load-audit column if simpler — do not change any existing business columns, keys, or the `FactEnrollment` grain).
2. Update `db/init/02_load_seed_data.sql` / the load path so the column populates at load time (default `now()` is sufficient; no need to backdate).
3. Add a `freshness:` block to the `raw` source in `models/staging/sources.yml` (e.g. `loaded_at_field: loaded_at`, `warn_after`/`error_after` thresholds consistent with the contract's 24-hour target).
4. Run `POSTGRES_PORT=55432 bash scripts/reset_phase1.sh` then `POSTGRES_PORT=55432 bash scripts/validate_phase1.sh` to confirm the reset/load path still works end to end.
5. Run `POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir .` and confirm it passes.
6. Run the full `dbt build` and confirm node/test counts only increase (should stay at 62 build nodes plus freshness checks, 0 errors).

### Option B — Explicitly scope-limit freshness (faster, also acceptable)
1. In `contracts/fact_enrollment.yml`, keep the `freshness.target` field but add a one-line note (e.g. a `freshness.enforcement: "Not automated — see Known Limitations"` key, or a comment) making clear it is a policy target, not a currently-tested guarantee.
2. Add an explicit "Known Limitations" bullet to `docs/phase4/setup.md` and `README.md` stating that freshness is a declared target without an automated dbt test in this synthetic, statically-regenerated demo, and why (no continuous ingestion to measure against).
3. Do not claim freshness testing is "implemented" anywhere in status docs.

### Either way
- Update `docs/implementation-status.md` (`Known Issues`, `Decisions Required`, `Next Action`) and this file (`Known Issues`, `Blockers`) to reflect the resolution.
- Re-run `dbt build` and record the exact pass/fail counts (do not round or approximate).
- Hand back to Claude for a short re-check of just this item before requesting the Phase 6 human governance gate.

---

## Recommended Next Action
Claude should review `docs/architecture.md`, `docs/setup.md`, `docs/demo.md`, and the README navigation against the Phase 6 documentation and demo requirements. Do not begin Phase 7 in this pass.

---

## Human Gate
Phase 6 implementation gate reached. Claude review is requested. Stop before Phase 7 Final QA until Claude review and the applicable human governance gate are complete.
- `git remote -v` reported the expected private GitHub origin for fetch and
  push.
- `git check-ignore -v .env` confirmed `.env` is ignored by `.gitignore`.
- Secret-pattern scans did not identify tracked real API keys, PATs, private
  keys, or production credentials.
- README.md describes the finished target state; the implementation artifacts it
  names are not present yet.
- Gemini completed Phase 0 review with PASS WITH CONDITIONS.
- All Gemini P0/P1/P2 findings have been addressed by Codex; no P0/P1/P2 findings remain for Phase 1.
- Phase 2 dbt and FactEnrollment implementation passed Gemini review.
- Phase 3 implementation is complete and ready for Gemini review.
- `git ls-files .DS_Store` returned no tracked file.
- `git check-ignore -v` confirmed ignores for `.env`, `.DS_Store`, `target/`,
  `dbt_packages/`, `logs/`, `.pytest_cache/`, and Python cache files.
- `.env.example` key validation found no nonconforming variable names.
- Secret-pattern scan returned no matches.

---

## Known Issues
- Docker Desktop's credential helper was not on the shell `PATH`; validation used `/Applications/Docker.app/Contents/Resources` in `PATH` without changing user configuration.
- The default host port `5432` is occupied on this machine; use the documented `POSTGRES_PORT=55432` override locally when needed.
- Power BI Desktop is unavailable on this macOS environment; actual `.pbip`, `.pbix`, and rendered screenshot generation remains a documented manual step.
- No Power BI artifact is claimed beyond the checked-in specifications.

---

## Blockers
None for the Phase 5 specification implementation. Claude review is complete and P1-3 freshness enforcement is resolved and re-verified.

---

## Decisions Needed
Human should inspect and commit the current changes. Do not begin Phase 6 until explicit Phase 6 authorization is given.

---

## Gemini Review Follow-up
The complete Gemini Phase 1 review is recorded in `docs/handoff/gemini-review.md`. All identified P1 and P2 fixes have been implemented and verified. No P0, P1, or P2 findings remain for Phase 1.

Verification included:

- `raw.students.entry_term_id` foreign-key enforcement;
- dependency-correct seed loading;
- exact row-count assertions for all 11 tables;
- admissions, deposits, students, programs, and enrollment referential-integrity assertions;
- registration-grain duplicate detection;
- budget and course-section business uniqueness constraints;
- documented host-port collision handling.

---

## Claude Review Follow-up
Claude independently reviewed Phases 3–5 on 2026-08-16 (full report: `docs/handoff/claude-review.md`). Verdict: **READY WITH CONDITIONS** (0 P0, 3 P1, 4 P2).

Claude independently re-verified the Gemini Phase 4 `dbt build` claim (61/61 nodes) and confirmed the three `powerbi/*/report-spec.yml` files correctly reference the Phase 3 marts and Phase 4 certification/lineage metadata, with no fabricated `.pbip`/`.pbix`/screenshot artifacts.

Claude found and fixed, in-session, two P1 gaps within existing spec/fix authority (re-verified via `dbt build` and a 12-scenario test suite — see `docs/handoff/claude-review.md`):
1. `scripts/check_contract_changes.py` could not detect changes to certified-metric calculations or certification-status downgrades (it never inspected `semantic/metric_definitions.yml`). Added `compare_metrics()` and a top-level status-downgrade check.
2. The contract's `minimum_row_count: 1` was unenforced metadata. Added `tests/fact_enrollment_minimum_row_count.sql`, wired it into `contracts/fact_enrollment.yml` and `certification/catalog.yml`.

**P1-1 — RESOLVED 2026-08-16.** The human confirmed that Phase 4/5 authorization is recorded in the human's own git commits: `da65f14` ("Phase 4 build and review + human approval complete") and `ab12374` ("Claude has entered the chat for review of phase 5. Codex completed build for it"), both authored and committed personally by `MaxBrooks-BI <brooks.maxj@gmail.com>` on 2026-08-16. No further action needed.

**P1-3 — RESOLVED 2026-08-16.** Added `loaded_at` columns to all 11 raw tables, explicit seed-load column lists, and dbt source freshness thresholds. Reset/load passed, 11/11 freshness checks passed, and full dbt build passed 62/62 with 0 errors and 0 warnings.

---

## Revised Instructions for Codex

Human authorization for Phase 4 and Phase 5 is confirmed (commits `da65f14`, `ab12374`). Do **not** re-raise or re-litigate P1-1. The single remaining item before Phase 6 is **P1-3 (freshness enforcement)**. Pick one of the two options below — either is acceptable to Claude — implement it, then hand back for a short re-check. Do not begin Phase 6 work in the same pass; stop after this item and update the status docs.

### Option A — Implement a real freshness check (preferred if time allows)
1. Add a `loaded_at timestamptz not null default now()` column to each `raw.*` table in `db/init/01_schema.sql` (or a single shared load-audit column if simpler — do not change any existing business columns, keys, or the `FactEnrollment` grain).
2. Update `db/init/02_load_seed_data.sql` / the load path so the column populates at load time (default `now()` is sufficient; no need to backdate).
3. Add a `freshness:` block to the `raw` source in `models/staging/sources.yml` (e.g. `loaded_at_field: loaded_at`, `warn_after`/`error_after` thresholds consistent with the contract's 24-hour target).
4. Run `POSTGRES_PORT=55432 bash scripts/reset_phase1.sh` then `POSTGRES_PORT=55432 bash scripts/validate_phase1.sh` to confirm the reset/load path still works end to end.
5. Run `POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir .` and confirm it passes.
6. Run the full `dbt build` and confirm node/test counts only increase (should stay at 62 build nodes plus freshness checks, 0 errors).

### Option B — Explicitly scope-limit freshness (faster, also acceptable)
1. In `contracts/fact_enrollment.yml`, keep the `freshness.target` field but add a one-line note (e.g. a `freshness.enforcement: "Not automated — see Known Limitations"` key, or a comment) making clear it is a policy target, not a currently-tested guarantee.
2. Add an explicit "Known Limitations" bullet to `docs/phase4/setup.md` and `README.md` stating that freshness is a declared target without an automated dbt test in this synthetic, statically-regenerated demo, and why (no continuous ingestion to measure against).
3. Do not claim freshness testing is "implemented" anywhere in status docs.

### Either way
- Update `docs/implementation-status.md` (`Known Issues`, `Decisions Required`, `Next Action`) and this file (`Known Issues`, `Blockers`) to reflect the resolution.
- Re-run `dbt build` and record the exact pass/fail counts (do not round or approximate).
- Hand back to Claude for a short re-check of just this item before requesting the Phase 6 human governance gate.

---

## Recommended Next Action
User: inspect and commit the completed Phase 5 plus Option A freshness changes. Then explicitly authorize Phase 6. P1-1 and P1-3 are resolved; no further fixes are required before the governance gate.

---

## Human Gate
Phase 5 reviewed by Claude with historical verdict READY WITH CONDITIONS. P1-3 freshness enforcement is now resolved via Option A and re-verified. Human should inspect and commit the current changes; stop before Phase 6 until explicit Phase 6 authorization.
- README.md describes the finished target state; the implementation artifacts it
  names are not present yet.
- Gemini completed Phase 0 review with PASS WITH CONDITIONS.
- All Gemini P0/P1/P2 findings have been addressed by Codex; no P0/P1/P2 findings remain for Phase 1.
- Phase 2 dbt and FactEnrollment implementation passed Gemini review.
- Phase 3 implementation is complete and ready for Gemini review.
- `git ls-files .DS_Store` returned no tracked file.
- `git check-ignore -v` confirmed ignores for `.env`, `.DS_Store`, `target/`,
  `dbt_packages/`, `logs/`, `.pytest_cache/`, and Python cache files.
- `.env.example` key validation found no nonconforming variable names.
- Secret-pattern scan returned no matches.

---

## Known Issues
- Docker Desktop's credential helper was not on the shell `PATH`; validation used `/Applications/Docker.app/Contents/Resources` in `PATH` without changing user configuration.
- The default host port `5432` is occupied on this machine; use the documented `POSTGRES_PORT=55432` override locally when needed.
- Power BI Desktop is unavailable on this macOS environment; actual `.pbip`, `.pbix`, and rendered screenshot generation remains a documented manual step.
- No Power BI artifact is claimed beyond the checked-in specifications.

---

## Blockers
None for the Phase 5 specification implementation. Claude review is complete and P1-3 freshness enforcement is resolved and re-verified.

---

## Decisions Needed
Human should inspect and commit the current changes. Do not begin Phase 6 until explicit Phase 6 authorization is given.

---

## Gemini Review Follow-up
The complete Gemini Phase 1 review is recorded in `docs/handoff/gemini-review.md`. All identified P1 and P2 fixes have been implemented and verified. No P0, P1, or P2 findings remain for Phase 1.

Verification included:

- `raw.students.entry_term_id` foreign-key enforcement;
- dependency-correct seed loading;
- exact row-count assertions for all 11 tables;
- admissions, deposits, students, programs, and enrollment referential-integrity assertions;
- registration-grain duplicate detection;
- budget and course-section business uniqueness constraints;
- documented host-port collision handling.

---

## Claude Review Follow-up
Claude independently reviewed Phases 3–5 on 2026-08-16 (full report: `docs/handoff/claude-review.md`). Verdict: **READY WITH CONDITIONS** (0 P0, 3 P1, 4 P2).

Claude independently re-verified the Gemini Phase 4 `dbt build` claim (61/61 nodes) and confirmed the three `powerbi/*/report-spec.yml` files correctly reference the Phase 3 marts and Phase 4 certification/lineage metadata, with no fabricated `.pbip`/`.pbix`/screenshot artifacts.

Claude found and fixed, in-session, two P1 gaps within existing spec/fix authority (re-verified via `dbt build` and a 12-scenario test suite — see `docs/handoff/claude-review.md`):
1. `scripts/check_contract_changes.py` could not detect changes to certified-metric calculations or certification-status downgrades (it never inspected `semantic/metric_definitions.yml`). Added `compare_metrics()` and a top-level status-downgrade check.
2. The contract's `minimum_row_count: 1` was unenforced metadata. Added `tests/fact_enrollment_minimum_row_count.sql`, wired it into `contracts/fact_enrollment.yml` and `certification/catalog.yml`.

**P1-1 — RESOLVED 2026-08-16.** The human confirmed that Phase 4/5 authorization is recorded in the human's own git commits: `da65f14` ("Phase 4 build and review + human approval complete") and `ab12374` ("Claude has entered the chat for review of phase 5. Codex completed build for it"), both authored and committed personally by `MaxBrooks-BI <brooks.maxj@gmail.com>` on 2026-08-16. No further action needed.

**P1-3 — RESOLVED 2026-08-16.** Added `loaded_at` columns to all 11 raw tables, explicit seed-load column lists, and dbt source freshness thresholds. Reset/load passed, 11/11 freshness checks passed, and full dbt build passed 62/62 with 0 errors and 0 warnings.

---

## Revised Instructions for Codex

Human authorization for Phase 4 and Phase 5 is confirmed (commits `da65f14`, `ab12374`). Do **not** re-raise or re-litigate P1-1. The single remaining item before Phase 6 is **P1-3 (freshness enforcement)**. Pick one of the two options below — either is acceptable to Claude — implement it, then hand back for a short re-check. Do not begin Phase 6 work in the same pass; stop after this item and update the status docs.

### Option A — Implement a real freshness check (preferred if time allows)
1. Add a `loaded_at timestamptz not null default now()` column to each `raw.*` table in `db/init/01_schema.sql` (or a single shared load-audit column if simpler — do not change any existing business columns, keys, or the `FactEnrollment` grain).
2. Update `db/init/02_load_seed_data.sql` / the load path so the column populates at load time (default `now()` is sufficient; no need to backdate).
3. Add a `freshness:` block to the `raw` source in `models/staging/sources.yml` (e.g. `loaded_at_field: loaded_at`, `warn_after`/`error_after` thresholds consistent with the contract's 24-hour target).
4. Run `POSTGRES_PORT=55432 bash scripts/reset_phase1.sh` then `POSTGRES_PORT=55432 bash scripts/validate_phase1.sh` to confirm the reset/load path still works end to end.
5. Run `POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt source freshness --project-dir . --profiles-dir .` and confirm it passes.
6. Run the full `dbt build` and confirm node/test counts only increase (should stay at 62 build nodes plus freshness checks, 0 errors).

### Option B — Explicitly scope-limit freshness (faster, also acceptable)
1. In `contracts/fact_enrollment.yml`, keep the `freshness.target` field but add a one-line note (e.g. a `freshness.enforcement: "Not automated — see Known Limitations"` key, or a comment) making clear it is a policy target, not a currently-tested guarantee.
2. Add an explicit "Known Limitations" bullet to `docs/phase4/setup.md` and `README.md` stating that freshness is a declared target without an automated dbt test in this synthetic, statically-regenerated demo, and why (no continuous ingestion to measure against).
3. Do not claim freshness testing is "implemented" anywhere in status docs.

### Either way
- Update `docs/implementation-status.md` (`Known Issues`, `Decisions Required`, `Next Action`) and this file (`Known Issues`, `Blockers`) to reflect the resolution.
- Re-run `dbt build` and record the exact pass/fail counts (do not round or approximate).
- Hand back to Claude for a short re-check of just this item before requesting the Phase 6 human governance gate.

---

## Recommended Next Action
User: inspect and commit the completed Phase 5 plus Option A freshness changes. Then explicitly authorize Phase 6. P1-1 and P1-3 are resolved; no further fixes are required before the governance gate.

---

## Human Gate
Phase 5 reviewed by Claude with historical verdict READY WITH CONDITIONS. P1-3 freshness enforcement is now resolved via Option A and re-verified. Human should inspect and commit the current changes; stop before Phase 6 until explicit Phase 6 authorization.
