# NSU BI Modernization Demo

A reproducible interview demonstration of a governed institutional BI and data
products operating model.

The demo shows how institutional data can move from source-system extracts into
a local analytical foundation, tested dbt transformations, certified semantic
definitions, lineage, quality gates, and Power BI-ready data products.

This is a demonstration project. It is not an NSU production implementation and
does not use real NSU data.

## What This Demonstrates

This repository is designed to support a BI / data products modernization
conversation around trust, governance, repeatability, and institutional
decision-making.

It demonstrates:

- A synthetic higher-education data foundation in PostgreSQL
- Deterministic seed data for schools, programs, students, terms, applications,
  admissions, deposits, registrations, enrollment, sections, and finance
- dbt models organized from source to staging, intermediate, marts, and certified
  products
- A governed `FactEnrollment` model with an explicit registration-level grain
- Certified semantic definitions for admissions and enrollment measures
- Data contracts, quality tests, and release-style certification metadata
- Lineage from source data through transformation, semantic definition, and
  Power BI consumption
- Change-management examples for schema, logic, dependency, metric, and grain
  changes
- Power BI / PBIP-ready assets for interview walkthroughs

## Architecture

```text
Synthetic source data
  -> PostgreSQL foundation
  -> dbt sources
  -> dbt staging models
  -> dbt intermediate models
  -> dimensions and facts
  -> certified models
  -> semantic definitions
  -> quality and contract gates
  -> lineage and certification metadata
  -> Power BI data products
```

PostgreSQL is used as the local demonstration database. SQL Server remains the
conceptual current-state source environment for the interview narrative.

## Technology Stack

- Docker and Docker Compose
- PostgreSQL
- dbt
- Python
- Power BI / PBIP artifacts where practical
- Git
- Markdown documentation for governance, contracts, lineage, and handoffs

## Repository Structure

```text
.
|-- README.md
|-- AGENTS.md
|-- CLAUDE.md
|-- docker-compose.yml
|-- dbt_project.yml
|-- seeds/
|-- scripts/
|-- models/
|   |-- sources/
|   |-- staging/
|   |-- intermediate/
|   |-- marts/
|   `-- certified/
|-- tests/
|-- semantic/
|-- contracts/
|-- lineage/
|-- certification/
|-- powerbi/
`-- docs/
    |-- CODEX_IMPLEMENTATION_SPEC.md
    |-- CLAUDE_REVIEW_SPEC.md
    |-- implementation-status.md
    `-- handoff/
```

The authoritative implementation status is maintained in
[docs/implementation-status.md](docs/implementation-status.md).

## Quick Start

Prerequisites:

- Docker Desktop
- Git
- Python 3
- dbt with the PostgreSQL adapter
- Power BI Desktop for optional PBIP review

Clone the repository:

```bash
git clone https://github.com/MaxBrooks-NovaTech/nsu-modernization-demo.git
cd nsu-modernization-demo
```

Start the local database:

```bash
docker compose up -d
```

Generate or load deterministic synthetic data:

```bash
python scripts/generate_synthetic_data.py
python scripts/load_seed_data.py
```

Run dbt:

```bash
dbt deps
dbt seed
dbt run
dbt test
dbt docs generate
```

Open dbt documentation:

```bash
dbt docs serve
```

Reset the demo database:

```bash
docker compose down -v
docker compose up -d
dbt seed
dbt run
dbt test
```

## Synthetic Data

The demo uses deterministic synthetic data only.

Included subject areas:

- Schools
- Programs
- Students
- Academic terms
- Course sections
- Applications
- Admissions
- Deposits
- Registrations
- Enrollment
- Financial and budget data

The dataset includes all 12 schools required by the implementation
specification. No real student, employee, financial, credential, or connection
data is permitted in this repository.

## Core Data Product

The principal certified model is `FactEnrollment`.

Required grain:

```text
One row = one student registration in one section for one academic term.
```

The grain is intentionally registration-level so the model can support section,
term, program, school, census, and IPEDS-oriented enrollment questions without
accidental fan-out.

## Governed Semantic Definitions

The semantic layer documents one governed definition per institutional question.

Certified definitions include:

- Applications
- Admits
- Deposits
- Enrolled
- Yield
- Census Enrollment
- IPEDS Enrollment

Each semantic definition includes:

- Definition
- Grain
- Owner
- Steward
- Source
- Calculation
- Sensitivity
- Certification status

## Data Quality

The project demonstrates quality as an operating control, not just a cleanup
step.

Quality coverage includes:

- Not-null checks
- Uniqueness checks
- Referential integrity
- Accepted values
- Duplicate detection
- Freshness checks
- Row-count anomaly checks
- Business-rule tests

The certified data product is expected to pass its required tests before it is
treated as certified for consumption.

## Data Contracts

The principal certified model has an explicit data contract covering:

- Model purpose
- Grain
- Schema
- Required fields
- Freshness expectations
- Quality rules
- Owner and steward
- Version
- Breaking-change policy

Contract changes are treated as governed changes, especially when they affect
grain, certified metrics, or downstream consumers.

## Lineage

The lineage documentation is designed to answer:

```text
If a source changes, which certified data products and reports are affected?
```

The demo traces:

```text
Source
  -> transformation
  -> certified model
  -> semantic definition
  -> report
```

This supports the interview narrative around moving from disconnected reporting
logic to governed, traceable data products.

## Certification

Certification is modeled as a release control.

A certified product includes:

- Owner
- Steward
- Governed definition
- Data contract
- Passing tests
- Lineage
- Version
- Certification status

Certified status should not be treated as a label alone. It represents a
repeatable review point before data is promoted for institutional consumption.

## Change Management

The demo includes examples of how to identify and evaluate:

- Optional schema additions
- Breaking schema changes
- Logic changes
- Dependency changes
- Grain changes
- Certified metric definition changes

Changes to certified metrics or fact grain require explicit human approval.

## Power BI Data Products

The planned Power BI / PBIP outputs are:

1. Executive Enrollment & Admissions
2. Institutional Data Trust
3. Data Lineage & Certification

Where manual Power BI Desktop work is required, the step is documented rather
than represented as automated.

## Demo Walkthrough

A typical interview walkthrough:

1. Start with the modernization problem: many reports, many definitions, uneven
   trust.
2. Show the synthetic source data and explain why the demo is isolated from
   production.
3. Start PostgreSQL with Docker to demonstrate reproducibility.
4. Run dbt models and tests.
5. Open `FactEnrollment` and explain the registration-level grain.
6. Review semantic definitions for applications, admits, deposits, enrollment,
   yield, census enrollment, and IPEDS enrollment.
7. Show the data contract and quality gates.
8. Walk through lineage from source to certified model to report.
9. Explain certification as a release gate.
10. Discuss how change detection protects downstream consumers.
11. Open the Power BI / PBIP artifacts and connect the governed model to
    institutional decision-making.

## Governance Rules

- Use synthetic data only.
- Never import real NSU student data.
- Never import real employee data.
- Never import real financial data.
- Never store NSU credentials or production connection strings.
- Do not imply the local PostgreSQL database is NSU production.
- Do not change certified metric definitions without human approval.
- Do not change the `FactEnrollment` grain without human approval.
- Keep implementation status and handoff documents current.

## Operating Model

Codex is the primary implementation agent. Claude is the independent reviewer.
The human user is the final governance authority.

The project workflow is:

```text
Build
  -> test
  -> document
  -> Codex handoff
  -> Claude review
  -> fix valid P0/P1 findings
  -> re-test
  -> next phase or human gate
```

## Documentation and Demo
- [Architecture](docs/architecture.md)
- [Data dictionary](docs/data-dictionary.md)
- [Setup](docs/setup.md)
- [Data dictionary](docs/data-dictionary.md)
- [Interview demo runbook](docs/demo.md)
- [Phase 4 lineage](docs/phase4/lineage.md)
- [Certification catalog](certification/catalog.yml)
- [Power BI specifications](powerbi/README.md)

## Key Documents
- [Implementation specification](docs/CODEX_IMPLEMENTATION_SPEC.md)
- [Independent review specification](docs/CLAUDE_REVIEW_SPEC.md)
- [Implementation status](docs/implementation-status.md)
- [Codex handoff](docs/handoff/codex-handoff.md)
- [Claude review](docs/handoff/claude-review.md)
- [Gemini review](docs/handoff/gemini-review.md)

## Publication

The repository remote is:

```text
https://github.com/MaxBrooks-NovaTech/nsu-modernization-demo.git
```

The repository is intended to be published privately unless the owner explicitly
chooses a public release policy.

## License

No license has been selected. Treat this repository as private and confidential
unless a license and publication policy are added by the owner.
