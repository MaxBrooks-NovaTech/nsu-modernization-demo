# GETTING_STARTED.md

# NSU BI Interview Demonstration
# Human Startup Procedure

---

## OBJECTIVE

Get Codex and Claude into a controlled autonomous:

BUILD
→ TEST
→ REVIEW
→ FIX
→ RE-TEST
→ REVIEW

loop.

The human should only intervene at:

- architecture decisions;
- scope decisions;
- destructive operations;
- major blockers;
- designated review gates;
- final interview preparation.

---

# STEP 1 — OPEN THE REPOSITORY

Open the NSU demonstration repository in VS Code.

Confirm:

AGENTS.md
CLAUDE.md

exist at the root.

Confirm:

docs/

exists.

---

# STEP 2 — VERIFY CONTROL FILES

Confirm:

docs/CODEX_IMPLEMENTATION_SPEC.md
docs/CLAUDE_REVIEW_SPEC.md
docs/implementation-status.md

and:

docs/handoff/codex-handoff.md
docs/handoff/claude-review.md

exist.

---

# STEP 3 — VERIFY GIT

Run:

git status

Do not proceed until you understand the current state.

---

# STEP 4 — START CODEX

Open Codex in VS Code.

Send:

"Read AGENTS.md and docs/CODEX_IMPLEMENTATION_SPEC.md.

Do not modify anything yet.

Inspect the repository and provide:

1. current repository state;
2. existing implementation;
3. missing components;
4. current implementation phase;
5. dependencies;
6. potential blockers.

Do not make changes."

---

# STEP 5 — REVIEW CODEX'S AUDIT

If Codex identifies an unexpected architecture or scope issue:

STOP.

Resolve it manually.

Otherwise continue.

---

# STEP 6 — AUTHORIZE THE FIRST BUILD

Send:

"Begin Phase 0.

Work autonomously within AGENTS.md and
docs/CODEX_IMPLEMENTATION_SPEC.md.

At completion:

1. update docs/implementation-status.md;
2. update docs/handoff/codex-handoff.md;
3. stop or hand off for Claude review as specified."

---

# STEP 7 — START CLAUDE REVIEW

Open Claude in the project environment.

Tell Claude:

"Read CLAUDE.md.

Read:

docs/implementation-status.md
docs/handoff/codex-handoff.md
docs/CODEX_IMPLEMENTATION_SPEC.md
docs/CLAUDE_REVIEW_SPEC.md

Review the current Codex work.

Inspect the actual repository.

Do not blindly trust the Codex handoff.

Produce/update:

docs/handoff/claude-review.md

Do not redesign the architecture.

Return only actionable P0/P1 findings unless P2 is important."

---

# STEP 8 — AUTONOMOUS LOOP

If Claude finds valid P0/P1 issues:

Tell Codex:

"Read docs/handoff/claude-review.md.

Address all valid P0/P1 findings that are within the current
specification.

Do not change architecture or scope.

Run all relevant tests.

Update:

docs/implementation-status.md
docs/handoff/codex-handoff.md

Then stop for Claude re-review."

Claude reviews again.

Repeat until:

PASS

or:

HUMAN DECISION REQUIRED

---

# STEP 9 — AUTHORIZE THE NEXT RANGE

Once a phase is clean, tell Codex:

"Continue through Phase X.

Use the autonomous Codex → Claude review loop.

Stop only when:

1. Phase X is complete;
2. a human decision is required;
3. a P0 cannot be resolved within the specification;
4. a destructive operation is required;
5. a major architectural change is required."

---

# STEP 10 — HUMAN REVIEW GATE

When the authorized range is complete:

STOP.

Review:

docs/implementation-status.md

docs/handoff/codex-handoff.md

docs/handoff/claude-review.md

Then inspect:

- Git diff;
- demo;
- Power BI;
- documentation.

Ask:

"Would I confidently defend this architecture to Cindy Gross,
Evelyn Hulce, and Amanda Miller?"

---

# STEP 11 — PANEL-SPECIFIC CHECK

Before the final gate, make sure the demo can answer:

## Financial Systems

How does this avoid breaking existing reporting?

How are costs measured?

Who owns capacity?

How are downstream consumers protected?

## Student Systems

How does Banner flow into SQL Server?

How is student data protected?

How do you handle conflicting definitions?

How do you handle academic-record changes?

## Budget

How do you justify platform investment?

How do you measure value?

What is the cost of Fabric capacity?

What gets retired?

---

# STEP 12 — FINAL DEMO TEST

Run the entire workflow from a clean state.

Verify:

1. PostgreSQL starts.
2. Synthetic data loads.
3. dbt runs.
4. Tests pass.
5. FactEnrollment is correct.
6. Semantic definitions exist.
7. Contracts exist.
8. Lineage works.
9. Certification works.
10. Change detection works.
11. Power BI works where applicable.
12. Documentation matches reality.

---

# STEP 13 — FINAL HUMAN REVIEW

Ask Claude:

"Perform final adversarial review using CLAUDE.md and
CLAUDE_REVIEW_SPEC.md.

Review the entire project as if you were:

1. Director, Financial Systems and Special Projects;
2. Executive Director, Student Systems and Academic Records;
3. University Budget Director.

Identify anything that could undermine my credibility in the interview.

Do not add scope.

Return READY, READY WITH CONDITIONS, NOT READY, or BLOCKED."

---

# STEP 14 — STOP BUILDING

Once Claude says:

READY

STOP.

Do not keep adding features.

Use the remaining time to rehearse.

---

# FINAL INTERVIEW NARRATIVE

The demo should support this story:

"We have legacy systems and multiple consumers.

The answer isn't simply another dashboard.

The answer is to establish governed data products with:

- explicit grain;
- shared definitions;
- quality controls;
- contracts;
- lineage;
- certification;
- controlled change;
- reusable semantic models.

That allows BI to become a sustainable institutional capability."

---

# HUMAN COMMANDS

Use:

"START"

to begin.

"CONTINUE THROUGH PHASE X"

to authorize additional work.

"STOP"

to immediately halt.

"REVIEW"

to request human review.

"FIX CLAUDE FINDINGS"

to authorize Codex to address the current review.

"FINAL REVIEW"

to trigger final QA.

"STOP BUILDING"

to end implementation and move to interview preparation.