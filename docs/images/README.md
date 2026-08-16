# Visual Evidence

Real screenshots of the running project, so the governed model, column-level documentation, lineage, and loaded data are visible without a live walkthrough. All content shown is real output from this repository's actual dbt project and PostgreSQL container — none of it is mocked, invented, or hand-drawn.

| File | What it shows | How it was generated |
| --- | --- | --- |
| `dbt-docs-overview.png` | The dbt docs site welcome/navigation page | `dbt docs generate` + `dbt docs serve`, screenshot of `http://localhost:8180/` |
| `dbt-docs-fact-enrollment-columns.png` | `FactEnrollment`'s real column list, types, descriptions, and test badges, as dbt actually reports them | Same dbt docs site, `fact_enrollment` model page, "Columns" tab |
| `dbt-docs-lineage-graph.png` | The real, expanded lineage graph for `fact_enrollment`: `raw.*` sources → `stg_*` → `int_registration_context` → `fact_enrollment` → its 3 tests | Same dbt docs site, clicked "View Lineage Graph" then the expand control |
| `semantic-metric-definitions.png` | The 7 governed metric definitions from `semantic/metric_definitions.yml` (definition, grain, source, calculation, certification status) | A local HTML rendering of that file's real content — see note below |
| `postgres-tables.png` | The actual `raw` and `analytics` schema tables in the running PostgreSQL container, `FactEnrollment`'s real column/type list, and 8 real sample rows | A local HTML rendering of real `psql` output (`docker compose exec postgres psql ...`) — see note below |
| `dbt-build-log.png` | A real `dbt build` terminal run: model creation, `FactEnrollment`'s grain/quality tests, and the final `PASS=62 WARN=0 ERROR=0` summary | Captured `dbt build` output on 2026-08-16, rendered as a terminal-style block — see note below |
| `dashboard-quality-metrics-summary.png` | A quality/metrics dashboard mockup: test pass count, certification status, and current values for all 7 governed metrics (Applications, Admits, Deposits, Yield, Enrolled, Census Enrollment, IPEDS Enrollment) | A local HTML rendering of real values queried live from the database and the real last `dbt build` result — see note below |
| `data-contract.png` | The full `FactEnrollment` data contract: version, status, owner, steward, grain, freshness target, required fields, required tests, breaking-change rules, and consumer | A local HTML rendering of `contracts/fact_enrollment.yml`'s real content — see note below |
| `change-management-detection.png` | Change detection actually catching a breaking change: an unchanged-contract baseline run (passes, exit 0) next to a required-field-removal run (`breaking: required field removed: registration_id`, exit 1) | Two real runs of `scripts/check_contract_changes.py` captured verbatim, rendered as a terminal-style block — see note below |
| `legacy-vs-certified-enrollment.png` | The "before" picture: four real, different answers to "how many students are enrolled this Fall?" from four synthetic Argos-style reports (376 / 188 / 188 / 188), none with a documented definition, next to the one certified answer (336) | A local HTML rendering of real query results against this project's own data — see `docs/legacy-reporting/README.md` for the exact queries |

## Why some of these are "rendered," not native screenshots

dbt Core's docs site only renders resources declared in its own schema (models, sources, tests, macros). `semantic/metric_definitions.yml` and `contracts/fact_enrollment.yml` are custom governance artifacts this project maintains outside dbt's schema (see `docs/architecture.md`), so neither has a native dbt docs page. Likewise, there is no GUI database client installed in this environment to screenshot directly, and `dashboard-quality-metrics-summary.png` stands in for the Power BI "Institutional Data Trust" page, which requires Power BI Desktop (see `PowerBIDashboard.md`) — unavailable on macOS. For all of these, the fix was **not** to skip them or fake a UI that doesn't exist — it was to render the *real* file/query/log/command-output content as a simple local HTML page and screenshot that, clearly labeled as such directly on each image. Every number and message in `semantic-metric-definitions.png`, `postgres-tables.png`, `dbt-build-log.png`, `dashboard-quality-metrics-summary.png`, `data-contract.png`, and `change-management-detection.png` is copied verbatim from a real file, a real `psql` session, a real `dbt build` run, or a real invocation of `scripts/check_contract_changes.py`; nothing is illustrative or approximated. `dashboard-quality-metrics-summary.png` in particular is explicitly labeled on the image itself as "not a native Power BI screenshot" so it's never mistaken for one.

## Reproducing these

```bash
# dbt docs screenshots
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt docs generate --project-dir . --profiles-dir .
POSTGRES_PORT=55432 .venv/bin/dbt docs serve --project-dir . --profiles-dir . --port 8180
# then open http://localhost:8180/ and navigate to a model's Columns tab / lineage graph

# postgres table listing and sample rows shown in postgres-tables.png
docker compose exec -T postgres psql -U nsu_demo_user -d nsu_modernization_demo -c '\dt raw.*' -c '\dt analytics.*'
docker compose exec -T postgres psql -U nsu_demo_user -d nsu_modernization_demo -c '\d analytics."FactEnrollment"'

# change detection scenarios shown in change-management-detection.png
python3 scripts/check_contract_changes.py contracts/fact_enrollment.yml contracts/fact_enrollment.yml
# (then repeat against a temporary copy with a required field removed — see docs/demo.md step 9 for the exact script)
```
