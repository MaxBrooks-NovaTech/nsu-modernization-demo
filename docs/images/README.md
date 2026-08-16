# Visual Evidence

Real screenshots of the running project, so the governed model, column-level documentation, lineage, and loaded data are visible without a live walkthrough. All content shown is real output from this repository's actual dbt project and PostgreSQL container — none of it is mocked, invented, or hand-drawn.

| File | What it shows | How it was generated |
| --- | --- | --- |
| `dbt-docs-overview.png` | The dbt docs site welcome/navigation page | `dbt docs generate` + `dbt docs serve`, screenshot of `http://localhost:8180/` |
| `dbt-docs-fact-enrollment-columns.png` | `FactEnrollment`'s real column list, types, descriptions, and test badges, as dbt actually reports them | Same dbt docs site, `fact_enrollment` model page, "Columns" tab |
| `dbt-docs-lineage-graph.png` | The real, expanded lineage graph for `fact_enrollment`: `raw.*` sources → `stg_*` → `int_registration_context` → `fact_enrollment` → its 3 tests | Same dbt docs site, clicked "View Lineage Graph" then the expand control |
| `semantic-metric-definitions.png` | The 7 governed metric definitions from `semantic/metric_definitions.yml` (definition, grain, source, calculation, certification status) | A local HTML rendering of that file's real content — see note below |
| `postgres-tables.png` | The actual `raw` and `analytics` schema tables in the running PostgreSQL container, `FactEnrollment`'s real column/type list, and 8 real sample rows | A local HTML rendering of real `psql` output (`docker compose exec postgres psql ...`) — see note below |

## Why two of these are "rendered," not native screenshots

dbt Core's docs site only renders resources declared in its own schema (models, sources, tests, macros). `semantic/metric_definitions.yml` is a custom governance artifact this project maintains outside dbt's schema (see `docs/architecture.md`), so it has no native dbt docs page. Likewise, there is no GUI database client installed in this environment to screenshot directly. For both, the fix was **not** to skip them or fake a UI that doesn't exist — it was to render the *real* file/query content as a simple local HTML page and screenshot that, clearly labeled as such. Every number, name, and value in `semantic-metric-definitions.png` and `postgres-tables.png` is copied verbatim from the real files and a real `psql` session against the running container; nothing is illustrative or approximated.

## Reproducing these

```bash
# dbt docs screenshots
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt docs generate --project-dir . --profiles-dir .
POSTGRES_PORT=55432 .venv/bin/dbt docs serve --project-dir . --profiles-dir . --port 8180
# then open http://localhost:8180/ and navigate to a model's Columns tab / lineage graph

# postgres table listing and sample rows shown in postgres-tables.png
docker compose exec -T postgres psql -U nsu_demo_user -d nsu_modernization_demo -c '\dt raw.*' -c '\dt analytics.*'
docker compose exec -T postgres psql -U nsu_demo_user -d nsu_modernization_demo -c '\d analytics."FactEnrollment"'
```
