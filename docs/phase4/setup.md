# Phase 4 — Lineage, Certification & Change Management

Phase 4 implements end-to-end data lineage mapping, institutional certification release gating, and automated data contract change detection for the NSU demonstration platform.

## Purpose & Scope

Phase 4 delivers the operational governance mechanisms required to manage change and maintain institutional trust:

1. **End-to-End Lineage**: Traces data flow from conceptual Banner / SQL Server sources through dbt models and semantic metrics to downstream consumers.
2. **Certification Release Gate**: Treats data certification as a verifiable operational release control rather than decorative metadata.
3. **Contract Change Management**: Automatically detects breaking schema, grain, and test changes in data contracts before releases reach production consumers.

---

## Core Artifacts

- **Lineage Architecture Document**: `docs/phase4/lineage.md`
  - Defines the 5-tier lineage architecture: Conceptual Source -> Landing (`raw`) -> Staging/Intermediate -> Certified Marts -> Semantic Definitions -> Consumers.
  - Documents product-specific lineage and impact analysis for `FactEnrollment`, `fact_recruitment_funnel`, and `fact_census_enrollment`.
- **Certification Catalog**: `certification/catalog.yml`
  - Operational governance catalog covering all 3 certified data products and 7 semantic metrics.
  - Specifies ownership (`Institutional Research and Analytics`), stewardship (`Data Governance Lead`), model definitions, required test suites, lineage references, downstream consumers, and formal approval.
- **Contract Change Detection Tool**: `scripts/check_contract_changes.py`
  - Python CLI tool comparing base vs. target contract YAML specifications.
  - Detects breaking changes (field removals, grain shifts, test omissions, rule modifications) and logs non-breaking additions.

---

## How to Run & Verify Phase 4

### 1. Verify Contract Integrity (No Changes)

```bash
python3 scripts/check_contract_changes.py contracts/fact_enrollment.yml contracts/fact_enrollment.yml
```

_Expected output_: `No breaking contract changes detected.` (Exit code: `0`)

### 2. Verify Breaking-Change Detection

Run the automated contract comparison test suite across all 6 validation scenarios:

```bash
python3 -c "
import subprocess, tempfile, yaml, copy

with open('contracts/fact_enrollment.yml') as f:
    base = yaml.safe_load(f)

def run_check(c1, c2):
    with tempfile.NamedTemporaryFile('w', suffix='.yml') as f1, tempfile.NamedTemporaryFile('w', suffix='.yml') as f2:
        yaml.dump(c1, f1)
        yaml.dump(c2, f2)
        f1.flush()
        f2.flush()
        res = subprocess.run(['python3', 'scripts/check_contract_changes.py', f1.name, f2.name], capture_output=True, text=True)
        return res.returncode, res.stdout.strip()

# 1. Identical -> Exit 0
# 2. Field removed -> Exit 1 (breaking)
# 3. Grain modified -> Exit 1 (breaking)
# 4. Quality test removed -> Exit 1 (breaking)
# 5. Breaking rules modified -> Exit 1 (breaking)
# 6. Field added -> Exit 0 (info)
"
```

### 3. Verify Full Data Pipeline & Quality Suite

```bash
POSTGRES_PORT=55432 POSTGRES_PASSWORD=replace-with-local-demo-password \
  .venv/bin/dbt build --project-dir . --profiles-dir . --no-use-colors
```

_Expected output_: 61/61 nodes passing (12 views, 3 tables, 46 data tests, 0 errors, 0 warnings).

---

## Demonstration Narrative

- **"If Banner changes, what breaks?"**: `docs/phase4/lineage.md` maps upstream sources directly to mart models and semantic metrics, enabling immediate blast-radius impact analysis.
- **"Certification as a Release Gate"**: `certification/catalog.yml` proves that a data product cannot be certified or published without satisfying its contract, passing all dbt tests, and receiving Data Governance Lead sign-off.
- **"Preventing Silent Failures"**: `scripts/check_contract_changes.py` demonstrates CI/CD pipeline automation that blocks pull requests containing breaking schema or grain shifts.
