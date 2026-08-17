# CLAUDE_REVIEW_SPEC.md

# NSU BI / Data Products Demonstration
# Independent Review Specification
# Version 1.0

---

## 1. PURPOSE

This document defines what Claude must independently review.

It is NOT an implementation specification.

Codex builds according to:

docs/CODEX_IMPLEMENTATION_SPEC.md

Claude reviews according to this document.

---

## 2. REVIEW PRINCIPLES

Every review should answer:

1. Does it work?
2. Is it reproducible?
3. Is the data model correct?
4. Are definitions governed?
5. Can lineage be demonstrated?
6. Can changes be detected?
7. Is quality measurable?
8. Is certification meaningful?
9. Is the architecture sustainable?
10. Can the presenter defend it to institutional stakeholders?

---

## 3. PHASE 0 REVIEW

Review:

- repository;
- architecture;
- scope;
- dependencies;
- documentation;
- duplication;
- implementation gaps.

Pass condition:

A clean, understandable starting point exists.

---

## 4. PHASE 1 REVIEW — DATA FOUNDATION

Review:

- Docker;
- PostgreSQL;
- initialization;
- synthetic data;
- seed files;
- deterministic generation;
- referential integrity;
- 12-school representation;
- admissions;
- enrollment;
- finance.

Verify:

- no real NSU data;
- no production credentials;
- reproducible data;
- clean startup;
- clean restart.

---

## 5. PHASE 2 REVIEW — DBT

Review:

- sources;
- staging;
- intermediate models;
- dimensions;
- facts;
- tests;
- documentation.

### Critical test

fact_enrollment must have explicit grain:

"One row = one student registration in one section for one academic term."

Verify:

- duplicate prevention;
- registration status;
- withdrawals;
- terms;
- schools;
- programs;
- sections;
- census logic.

Ask:

"Can another analyst use this model without reimplementing enrollment
logic?"

---

## 6. PHASE 3 REVIEW — SEMANTIC LAYER

Review:

- definitions;
- glossary;
- owners;
- stewards;
- certification;
- sensitivity;
- contracts;
- quality.

Review at minimum:

- Applications;
- Admits;
- Deposits;
- Enrolled;
- Yield;
- Census Enrollment;
- IPEDS Enrollment.

The objective is:

ONE CERTIFIED DEFINITION PER QUESTION

not:

"Every number must be identical."

Legitimate differences must be explicitly documented.

---

## 7. DATA CONTRACT REVIEW

Verify:

- schema;
- grain;
- required fields;
- freshness;
- quality rules;
- owner;
- steward;
- consumer;
- version;
- breaking-change policy.

A contract must be actionable, not decorative.

---

## 8. DATA QUALITY REVIEW

Review:

- null checks;
- uniqueness;
- referential integrity;
- accepted values;
- freshness;
- row-count anomalies;
- duplicate detection;
- business rules.

Verify that tests actually execute.

---

## 9. LINEAGE REVIEW

Verify:

SOURCE
  ↓
TRANSFORMATION
  ↓
CERTIFIED MODEL
  ↓
SEMANTIC DEFINITION
  ↓
REPORT

Ask:

"If Banner changes, can we determine what downstream products are
affected?"

The architecture should support current SQL Server lineage and eventual
Fabric integration.

---

## 10. CERTIFICATION REVIEW

Certification must be a release control.

Review:

- owner;
- definition;
- tests;
- lineage;
- approval;
- version;
- certification status;
- consumer impact.

A green badge without evidence is insufficient.

---

## 11. CHANGE MANAGEMENT REVIEW

Review:

- manifest;
- schema comparison;
- breaking-change detection;
- dependency impact;
- semantic changes;
- certification invalidation.

Test:

1. Add optional field.
2. Change description.
3. Change logic.
4. Remove required field.
5. Change fact grain.
6. Change certified metric definition.

---

## 12. POWER BI REVIEW

Review:

### Page 1
Executive Enrollment & Admissions

### Page 2
Institutional Data Trust

### Page 3
Data Lineage & Certification

Review:

- correctness;
- usability;
- filtering;
- metric definitions;
- certification;
- freshness;
- lineage;
- school coverage;
- admissions funnel.

PBIP should demonstrate engineering/source-control thinking.

---

## 13. DOCUMENTATION REVIEW

Verify:

- README;
- architecture;
- setup;
- semantic definitions;
- contracts;
- lineage;
- certification;
- demo script;
- known limitations.

Documentation must describe what actually exists.

---

## 14. READINESS REVIEW

Evaluate whether the candidate can credibly explain:

### Financial Systems

- cost;
- ROI;
- capacity;
- downstream reporting;
- reconciliation.

### Student Systems

- Banner;
- SQL Server;
- academic records;
- security;
- access;
- data quality;
- change management.

### Budget

- platform cost;
- Fabric capacity;
- TCO;
- value measurement.

The prep materials specifically identify questions around modernization
without breaking existing systems, security before touching production
student data, platform cost, downstream consumers, and conflicting
numbers. Use those as adversarial review scenarios.

---

## 15. ARCHITECTURE REVIEW

Review whether the architecture supports:

- current-state SQL Server;
- future Fabric;
- governance;
- lineage;
- certification;
- semantic reuse;
- data products;
- retirement of legacy reporting;
- incremental migration.

Do not recommend technology merely because it is newer.

---

## 16. P0 / P1 / P2

### P0

Blocks readiness.

### P1

Material weakness.

### P2

Optional improvement.

---

## 17. FINAL REVIEW

Final review must validate:

[ ] Data works.
[ ] dbt works.
[ ] Fact grain is correct.
[ ] Semantic definitions are governed.
[ ] Contracts exist.
[ ] Quality tests pass.
[ ] Lineage works.
[ ] Certification works.
[ ] Change detection works.
[ ] Power BI artifacts are real.
[ ] Documentation is accurate.
[ ] Demo is reproducible.
[ ] No real NSU data exists.
[ ] Narrative is defensible.

---

## 18. FINAL DECISION

Return exactly one:

READY
READY WITH CONDITIONS
NOT READY
BLOCKED