# Phase 2 Setup

Phase 2 adds a local dbt transformation layer over the synthetic `raw` schema.
It creates staging models, an intermediate registration context, and the
certified `analytics.fact_enrollment` table.

## Install dbt

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Configure the profile

Copy `profiles.yml.example` to `profiles.yml` in the project directory (or to
`~/.dbt/profiles.yml`). Set `POSTGRES_PASSWORD` in the shell before running dbt;
the profile reads the password from that environment variable. If PostgreSQL
is using the documented alternate port, change `port` to `55432`.

For the current local container:

```bash
export POSTGRES_PASSWORD=replace-with-local-demo-password
cp profiles.yml.example profiles.yml
sed -i '' 's/port: 5432/port: 55432/' profiles.yml
```

## Run Phase 2

```bash
dbt debug --project-dir . --profiles-dir .
dbt build --project-dir . --profiles-dir .
```

`fact_enrollment` grain: one row per student registration in one section for
one academic term. Its uniqueness is tested through `registration_id` and the
custom composite-grain test.
