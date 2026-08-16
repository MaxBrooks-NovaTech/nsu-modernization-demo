# CODEX_VSCODE_SETUP.md

# Installing Codex in VS Code

## 1. Prerequisites

You need:

- Visual Studio Code
- A supported operating system
- A ChatGPT account with Codex access
- Your project repository

The Codex IDE extension supports VS Code and compatible VS Code forks.

Windows support has historically been more limited than macOS/Linux, so
if running Windows, WSL may provide the better experience.

---

## 2. Install the Codex VS Code Extension

Open VS Code.

Open:

Extensions

Search for:

Codex

Install the official OpenAI Codex extension.

Alternatively use the VS Code extension identifier documented by OpenAI.

Do NOT install an unrelated third-party extension merely because it has
"Codex" in the name.

---

## 3. Sign In

Open the Codex panel in VS Code.

Sign in using the ChatGPT account that has Codex access.

A ChatGPT subscription can provide Codex access without requiring a
separate API key.

---

## 4. Open the Project

Open the root folder of the NSU demonstration repository.

IMPORTANT:

Open the repository root, not merely the docs directory.

Example:

/NSU-BI-Demo/

The following files should be visible at the root:

AGENTS.md
CLAUDE.md

---

## 5. Verify the Instructions

Before running Codex, verify:

AGENTS.md

exists at the repository root.

Then verify:

docs/CODEX_IMPLEMENTATION_SPEC.md

exists.

Then verify:

docs/implementation-status.md

exists.

Then verify:

docs/handoff/codex-handoff.md

exists.

---

## 6. Verify Git

Open the VS Code terminal.

Run:

git status

Confirm the repository is clean or that you understand the existing
changes.

Do NOT ask Codex to reset the repository unless you explicitly intend to
discard changes.

---

## 7. Start Codex in PLAN/CHAT MODE First

Before allowing implementation, ask Codex to:

"Read AGENTS.md and docs/CODEX_IMPLEMENTATION_SPEC.md. Inspect the
repository and report the current state. Do not modify files yet."

Review its response.

This is the initial architecture sanity check.

---

## 8. Start Implementation

Once satisfied, instruct:

"Read AGENTS.md, docs/CODEX_IMPLEMENTATION_SPEC.md, and
docs/implementation-status.md.

Begin Phase 0.

Work autonomously within the authorized scope.

Do not modify project architecture or expand scope without stopping for
human approval.

At completion, update implementation-status.md and
docs/handoff/codex-handoff.md."

---

## 9. Autonomous Mode

For the intended workflow, authorize Codex to work through a defined
phase range.

Example:

"Build through Phase 3. You may use the Codex → Claude review loop for
ordinary P0/P1 fixes. Stop when Phase 3 is complete or when a human
architectural decision is required."

---

## 10. Safety

Do NOT give unrestricted access unnecessarily.

The default Codex agent mode should be sufficient for most project work.

Be cautious with:

- network access;
- production credentials;
- filesystem access outside the repository;
- destructive shell commands.

This project should contain only synthetic data.

---

## 11. Stopping Codex

If necessary, stop the current Codex task/session.

Before stopping, instruct:

"Stop here. Preserve current work. Update implementation-status.md and
codex-handoff.md with the current state."

---

## 12. Resuming

Open the same project.

Tell Codex:

"Read AGENTS.md, implementation-status.md, codex-handoff.md, and any
claude-review.md. Resume from the documented state. Do not restart
completed work."

---

## 13. Claude Review

Claude should review:

docs/handoff/codex-handoff.md

and:

docs/handoff/claude-review.md

Codex should then consume valid P0/P1 findings.

---

## 14. Important

Do not put the changing project status inside AGENTS.md.

AGENTS.md = operating rules.

CODEX_IMPLEMENTATION_SPEC.md = project requirements.

implementation-status.md = current state.

codex-handoff.md = latest Codex handoff.

claude-review.md = latest Claude review.