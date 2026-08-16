# Quickstart — Running This Demo Yourself

This is a from-scratch walkthrough for someone who has never set this project up before. If you already have Docker, Python, and Git, skip to [Step 4] (#step-4-clone-the-repository). Everything below runs on macOS, Windows, or Linux — a couple of steps have OS-specific notes, called out where they apply.

No prior dbt, PostgreSQL, or Docker experience is assumed. Every command below is copy-pasteable into a terminal (macOS: Terminal or iTerm; Windows: PowerShell or Command Prompt; either works).

## What you're installing, and why

| Tool | Why this demo needs it |
| --- | --- |
| **Docker Desktop** | Runs a local, disposable PostgreSQL database — no separate database server to install or manage. |
| **Python 3** | Runs the synthetic-data generator and the dbt transformation tool. |
| **Git** | Downloads (clones) this repository to your computer. |

## Step 1 — Install Docker Desktop

1. Go to <https://www.docker.com/products/docker-desktop/> and download Docker Desktop for your operating system (macOS, Windows, or Linux).
2. Run the installer and follow the prompts. On macOS, drag Docker to Applications; on Windows, the installer may ask to enable WSL2 — accept that if prompted.
3. Open Docker Desktop once after installing. Wait until it says it's running (the whale icon in your menu bar/system tray stops animating).
4. Verify it worked — open a terminal and run:

   ```bash
   docker --version
   ```

   You should see a version number, e.g. `Docker version 27.x.x`. If you see "command not found," Docker Desktop may still be starting up, or the installer needs a restart of your terminal/computer.

## Step 2 — Install Python 3

Most Macs and many Windows machines already have Python installed. Check first:

```bash
python3 --version
```

- If you see `Python 3.9` or newer, you're set — skip to Step 3.
- If you get an error, or a version below 3.9, install Python from <https://www.python.org/downloads/>. Download the latest Python 3 installer for your OS and run it.
  - **Windows only**: during install, check the box **"Add python.exe to PATH"** before clicking Install — this is easy to miss and means the `python3` command won't work afterward if skipped.
- Confirm `pip` (Python's package installer) came with it:

  ```bash
  python3 -m pip --version
  ```

  This should also print a version number. `pip` is installed automatically with Python 3.4+, so a separate install step usually isn't needed.

## Step 3 — Install Git (if you don't already have it)

```bash
git --version
```

If that errors, install Git from <https://git-scm.com/downloads> (macOS users can alternatively run `xcode-select --install` if prompted).

## Step 4 — Clone the repository

```bash
git clone https://github.com/MaxBrooks-NovaTech/nsu-modernization-demo.git
cd nsu-modernization-demo
```

(Use whichever remote URL you were given if it differs from the one above.)

## Step 5 — Create and activate a Python virtual environment

A "virtual environment" (venv) is a self-contained folder of Python packages just for this project, so it doesn't interfere with anything else on your computer. Create one once:

```bash
python3 -m venv .venv
```

This creates a `.venv/` folder inside the repository (already excluded from git — you won't see it show up when you commit anything).

**You do not need to "activate" the venv for the commands in this guide** — every command below calls `.venv/bin/python3` or `.venv/bin/pip` directly, which works the same on macOS/Linux. If you're on Windows and prefer PowerShell activation instead, run `.venv\Scripts\Activate.ps1` once per terminal session and then you can drop the `.venv/bin/` prefix from the commands below.

## Step 6 — Install the Python requirements

```bash
.venv/bin/pip install -r requirements.txt
```

This installs `dbt-core`, `dbt-postgres` (the tool that builds and tests the data models), and `types-PyYAML` (a small type-checking helper, not used at runtime). It'll take a minute or two the first time.

## Step 7 — Generate the synthetic data and start the database

```bash
python3 scripts/generate_synthetic_data.py
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
```

What this does: generates deterministic (same every time) fake student/enrollment/admissions data into `seeds/*.csv`, then starts a PostgreSQL database inside Docker and loads that data into it. `POSTGRES_PORT=55432` avoids a conflict if you already have something using PostgreSQL's default port `5432` — it's safe to always use this.

You should see a table of row counts print at the end (schools: 12, students: 240, etc.) with no errors.

**If this step fails immediately**: make sure Docker Desktop is actually running (Step 1) — check for the whale icon.

## Step 8 — Run dbt (build and test the data models)

```bash
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt debug --project-dir . --profiles-dir .
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors
```

The first command checks the connection; it should end with `All checks passed!`. The second builds all the models and runs all the quality tests — expect a line near the end like:

```text
Done. PASS=62 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=62
```

`docs/images/dbt-build-log.png` shows what a real successful run of this command looks like, if you want to compare.

## Step 9 — (Optional) Browse the generated documentation

```bash
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password .venv/bin/dbt docs generate --project-dir . --profiles-dir .
POSTGRES_PORT=55432 .venv/bin/dbt docs serve --project-dir . --profiles-dir . --port 8180
```

Then open <http://localhost:8180/> in a browser to explore the data model, column descriptions, and lineage graph interactively. Press `Ctrl+C` in the terminal to stop the server when you're done.

## You're done

At this point you have a working local copy of the entire demo: a PostgreSQL database with realistic synthetic data, dbt models and passing tests, and browsable documentation. From here:

- `docs/demo.md` — the interview walkthrough script (if present — it's a local-only file for the repository owner, not tracked in git).
- `docs/architecture.md` — how the pieces fit together.
- `docs/images/` — screenshots if you'd rather look than run things live.
- `PowerBIDashboard.md` (repository root, if present) — instructions for the Power BI portion, which requires Power BI Desktop on Windows separately.

## Resetting or starting over

If anything gets into a confusing state, this destroys and rebuilds the local database from scratch (your synthetic data, not anything real):

```bash
POSTGRES_PORT=55432 bash scripts/reset_phase1.sh
```

## Troubleshooting

| Problem | Likely fix |
| --- | --- |
| `docker: command not found` | Docker Desktop isn't installed or isn't running yet — see Step 1. |
| `python3: command not found` | Python isn't installed or isn't on your PATH — see Step 2 (Windows: reinstall and check the PATH box). |
| Something about port `5432` already in use | Expected — this guide always uses `POSTGRES_PORT=55432` specifically to avoid that. Make sure you included it in every command that needs it. |
| `dbt debug` fails to connect | Confirm Docker Desktop is running and `POSTGRES_PORT=55432 bash scripts/reset_phase1.sh` completed without errors first. |
| Anything else | Check `docs/setup.md` for more detail, or `docs/handoff/claude-review.md` for known issues already investigated. |
