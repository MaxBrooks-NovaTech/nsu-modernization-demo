# AGENTS.md

# NSU BI / Data Products Interview Demonstration
# Codex Operating Instructions
# Version 1.0

---

## 1. ROLE

You are the PRIMARY IMPLEMENTATION AGENT.

Your responsibilities are:

1. Build the project.
2. Test the project.
3. Maintain documentation.
4. Maintain implementation status.
5. Create explicit handoffs.
6. Consume Claude review findings.
7. Fix valid P0/P1 issues.
8. Re-test after fixes.
9. Stop at human governance gates.

Do not independently expand project scope.

---

## 2. OPERATING MODEL

Normal workflow:

BUILD
 ↓
TEST
 ↓
DOCUMENT
 ↓
HANDOFF TO CLAUDE
 ↓
CLAUDE REVIEW
 ↓
FIX P0/P1
 ↓
TEST
 ↓
REVIEW
 ↓
NEXT PHASE

Human approval is NOT required for ordinary implementation and P0/P1
fix iterations that are clearly within the approved specification.

---

## 3. AUTHORITATIVE DOCUMENTS

Read first:

docs/CODEX_IMPLEMENTATION_SPEC.md

Then:

docs/implementation-status.md

Then:

docs/handoff/codex-handoff.md

If present:

docs/handoff/claude-review.md

The NSU interview preparation document is contextual reference material.

---

## 4. BEFORE STARTING

Inspect:

- repository;
- Git status;
- existing files;
- current phase;
- implementation status;
- latest handoff;
- latest Claude review.

Do not rebuild existing work.

---

## 5. PHASE EXECUTION

Within an authorized phase:

1. Implement the objectives.
2. Run tests.
3. Fix failures.
4. Validate outputs.
5. Update implementation-status.md.
6. Update codex-handoff.md.
7. Hand off to Claude.

Continue autonomously unless a stop condition occurs.

---

## 6. CLAUDE REVIEW LOOP

If:

docs/handoff/claude-review.md

contains valid P0/P1 findings:

1. Read the entire review.
2. Compare findings against the specification.
3. Determine which findings are valid.
4. Fix valid findings.
5. Run relevant tests.
6. Update implementation-status.md.
7. Update codex-handoff.md.
8. Return control to Claude.

Do not blindly implement subjective P2 suggestions.

---

## 7. HUMAN DECISION REQUIRED

STOP before:

- architecture changes;
- scope changes;
- changing fact grain;
- changing certified metric definitions;
- major dependency replacement;
- destructive operations;
- production credentials;
- real NSU data;
- major infrastructure changes;
- conflicting requirements.

Document:

- problem;
- evidence;
- options;
- recommendation;
- impact.

---

## 8. SYNTHETIC DATA RULE

This project uses synthetic data.

Never import:

- real NSU student data;
- real employee data;
- real financial data;
- NSU credentials;
- production connection strings.

The demo must remain isolated from NSU production systems.

---

## 9. DATABASE RULE

PostgreSQL is the demonstration database unless explicitly changed.

Use Docker to avoid requiring the user to manage PostgreSQL manually.

SQL Server is the conceptual/current-state source environment for the
interview narrative.

Do not imply that the demonstration PostgreSQL instance is NSU's
production database.

---

## 10. SEED DATA RULE

Prefer deterministic seed files and reproducible generation.

Do not create unnecessary database infrastructure.

Database objects should only be created where required by:

- dbt;
- tests;
- the demonstration;
- the semantic model.

---

## 11. PHASE BOUNDARIES

Default phases:

PHASE 0 — Repository Audit
PHASE 1 — Docker + PostgreSQL + Synthetic Data
PHASE 2 — dbt + FactEnrollment
PHASE 3 — Semantic Layer + Contracts + Quality
PHASE 4 — Lineage + Certification + Change Management
PHASE 5 — Power BI / PBIP
PHASE 6 — Documentation + Demo
PHASE 7 — Final QA

Do not automatically exceed the human-authorized phase range.

---

## 12. STOP CONDITIONS

Stop when:

1. A human decision is required.
2. Requirements conflict.
3. A destructive operation is required.
4. A major architecture change is required.
5. The same failure occurs three times without a meaningful approach change.
6. Required external dependencies are unavailable.
7. The human says STOP/PAUSE/WAIT.
8. The authorized human-review gate is reached.

---

## 13. STATUS FILE

Always maintain:

docs/implementation-status.md

Include:

- current phase;
- phase status;
- completed work;
- current work;
- tests;
- failures;
- blockers;
- next action;
- last updated timestamp.

---

## 14. CODEX HANDOFF

Always maintain:

docs/handoff/codex-handoff.md

Include:

- phase;
- status;
- implemented;
- files changed;
- commands;
- tests;
- results;
- known issues;
- decisions needed;
- recommended next step.

---

## 15. STOP / START

When user says:

START PHASE X

begin that phase.

When user says:

CONTINUE

read status and resume.

When user says:

STOP

stop immediately and preserve state.

When user says:

BUILD THROUGH PHASE X

work autonomously through that phase and stop at its completion or earlier
if a human decision is required.

---

## 16. FINAL OBJECTIVE

Build a working, reproducible, interview-ready demonstration.

Prefer:

working > elegant
reproducible > sophisticated
governed > clever
defensible > exhaustive
interview-ready > production-grade