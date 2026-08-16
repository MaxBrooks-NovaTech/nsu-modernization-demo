#!/usr/bin/env bash
set -euo pipefail

# Exports the three certified analytics marts to seeds/mart_tables/*.csv so the
# Power BI portion of the demo can run against CSV snapshots without a live
# PostgreSQL connection. Run after `dbt build` so the marts are current.

OUT_DIR="seeds/mart_tables"
mkdir -p "$OUT_DIR"

docker compose exec -T postgres psql -U "${POSTGRES_USER:-nsu_demo_user}" -d "${POSTGRES_DB:-nsu_modernization_demo}" -v ON_ERROR_STOP=1 \
  -c "\copy (select * from analytics.\"FactEnrollment\" order by registration_id) to stdout with csv header" \
  > "$OUT_DIR/fact_enrollment.csv"

docker compose exec -T postgres psql -U "${POSTGRES_USER:-nsu_demo_user}" -d "${POSTGRES_DB:-nsu_modernization_demo}" -v ON_ERROR_STOP=1 \
  -c "\copy (select * from analytics.fact_recruitment_funnel order by application_id) to stdout with csv header" \
  > "$OUT_DIR/fact_recruitment_funnel.csv"

docker compose exec -T postgres psql -U "${POSTGRES_USER:-nsu_demo_user}" -d "${POSTGRES_DB:-nsu_modernization_demo}" -v ON_ERROR_STOP=1 \
  -c "\copy (select * from analytics.fact_census_enrollment order by enrollment_id) to stdout with csv header" \
  > "$OUT_DIR/fact_census_enrollment.csv"

echo "Exported mart CSVs to $OUT_DIR:"
wc -l "$OUT_DIR"/*.csv
