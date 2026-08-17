# CODEX_IMPLEMENTATION_SPEC.md

# NSU BI / Data Products Demonstration
# Implementation Specification
# Version 1.0

---

## 1. OBJECTIVE

Build a small but credible demonstration of a governed institutional BI
operating model.

The demonstration must show:

SOURCE
 ↓
DATA FOUNDATION
 ↓
TRANSFORMATION
 ↓
SEMANTIC MODEL
 ↓
QUALITY
 ↓
LINEAGE
 ↓
CERTIFICATION
 ↓
DATA PRODUCT
 ↓
CONSUMPTION

This is a demonstration project.

It is NOT an NSU production implementation.

---

## 2. TECHNOLOGY

Use:

- Docker;
- PostgreSQL;
- dbt;
- Python where useful;
- synthetic data;
- Power BI / PBIP where available;
- Git.

Do not require the user to manage a persistent PostgreSQL server manually.

---

## 3. DATABASE

Run PostgreSQL in Docker.

Provide:

- docker-compose.yml;
- initialization;
- deterministic seed data;
- reset capability.

SQL Server remains the conceptual source/current-state architecture.

---

## 4. SYNTHETIC DATA

Create synthetic:

- schools;
- programs;
- students;
- terms;
- sections;
- registrations;
- applications;
- admissions;
- deposits;
- enrollment;
- financial/budget data where needed.

Include all 12 schools.

Data must be deterministic.

---

## 5. DBT

Create:

sources
 ↓
staging
 ↓
intermediate
 ↓
dimensions/facts
 ↓
certified models

Include tests.

---

## 6. FACT ENROLLMENT

Create:

fact_enrollment

Required grain:

ONE ROW = ONE STUDENT REGISTRATION IN ONE SECTION FOR ONE ACADEMIC TERM.

Document the grain explicitly.

Do not allow accidental fan-out.

---

## 7. SEMANTIC DEFINITIONS

Create governed definitions for:

- Applications;
- Admits;
- Deposits;
- Enrolled;
- Yield;
- Census Enrollment;
- IPEDS Enrollment.

Each definition must include:

- definition;
- grain;
- owner;
- steward;
- source;
- calculation;
- sensitivity;
- certification status.

---

## 8. DATA CONTRACT

Create a contract for the principal certified model.

Include:

- schema;
- grain;
- required fields;
- freshness;
- quality;
- owner;
- version;
- breaking-change rules.

---

## 9. DATA QUALITY

Implement tests for:

- nulls;
- uniqueness;
- referential integrity;
- accepted values;
- duplicates;
- freshness;
- row-count anomalies;
- business rules.

---

## 10. LINEAGE

Implement enough lineage to demonstrate:

SOURCE
 ↓
TRANSFORMATION
 ↓
MODEL
 ↓
SEMANTIC DEFINITION
 ↓
REPORT

Document the architecture.

---

## 11. CERTIFICATION

Implement a demonstrable certification state.

A certified product should have:

- owner;
- definition;
- tests;
- lineage;
- status;
- version.

Certification should be treated as a release gate.

---

## 12. CHANGE DETECTION

Demonstrate detection of:

- optional additions;
- breaking schema changes;
- logic changes;
- dependency changes;
- grain changes;
- certified metric changes.

---

## 13. POWER BI

Where practical create PBIP artifacts for:

1. Executive Enrollment & Admissions.
2. Institutional Data Trust.
3. Data Lineage & Certification.

Do not fabricate screenshots or pretend artifacts exist.

If a manual Power BI Desktop step is unavoidable, document it.

---

## 14. DOCUMENTATION

Maintain:

- README;
- architecture;
- setup;
- data dictionary;
- semantic definitions;
- contracts;
- lineage;
- certification;
- demo instructions.

---

## 15. PROJECT STORY

The implementation should demonstrate:

"Governance is QA for data."

and:

"Certification is a release gate."

and:

"Build once, reuse many times."

The demonstration should show how BI becomes a sustainable data-product
operating model rather than another dashboard project.

---

## 16. NON-GOALS

Do not build:

- production NSU integrations;
- real student-data ingestion;
- enterprise authentication;
- full Fabric migration;
- full Purview deployment;
- production-grade infrastructure;
- unnecessary microservices;
- unnecessary databases.

---

## 17. PHASES

### Phase 0
Repository audit.

### Phase 1
Docker + PostgreSQL + synthetic data.

### Phase 2
dbt + fact_enrollment.

### Phase 3
Semantic layer + contracts + quality.

### Phase 4
Lineage + certification + change management.

### Phase 5
Power BI / PBIP.

### Phase 6
Documentation + demo.

### Phase 7
Final QA.

---

## 18. COMPLETION STANDARD

Prefer:

working;
reproducible;
simple;
defensible.

Do not sacrifice end-to-end functionality for optional sophistication.