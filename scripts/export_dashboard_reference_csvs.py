#!/usr/bin/env python3
"""Export certification, lineage, and quality-test evidence as CSVs for the
Institutional Data Trust and Data Lineage & Certification report pages.

These pages describe governance metadata (certification/catalog.yml,
docs/phase4/lineage.md) and real dbt test outcomes (target/run_results.json)
rather than transactional data, so they have no natural PostgreSQL table to
export from. This script turns those real sources into CSVs under
`data_governance/`, keeping governance/reference data separate from mart facts.

Run after `dbt build` so run_results.json reflects the current test run.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

OUT_DIR = Path("data_governance")


def export_certification_catalog() -> None:
    catalog = yaml.safe_load(Path("certification/catalog.yml").read_text())
    rows = []
    for product_key, product in catalog["products"].items():
        rows.append(
            {
                "product": product_key,
                "model": product["model"],
                "version": product["version"],
                "owner": catalog["owner"],
                "steward": catalog["steward"],
                "status": product["status"],
                "last_reviewed": catalog["last_reviewed"],
                "approver_role": product["approval"]["approver_role"],
                "approval_decision": product["approval"]["decision"],
                "consumers": "; ".join(product["consumers"]),
                "semantic_definitions": "; ".join(product["semantic_definitions"]),
            }
        )
    _write_csv(OUT_DIR / "certification_catalog.csv", rows)


def export_lineage_summary() -> None:
    # Transcribed from docs/phase4/lineage.md's "Certified product lineage" table.
    rows = [
        {
            "product": "fact_enrollment",
            "source_entities": "raw.registrations, raw.course_sections, raw.students, raw.terms, raw.schools, raw.programs",
            "model": "analytics.FactEnrollment",
            "semantic_definitions": "enrolled",
            "consumers": "Executive Enrollment and Admissions reporting; downstream enrollment analysis",
        },
        {
            "product": "recruitment_funnel",
            "source_entities": "raw.applications, raw.admissions, raw.deposits",
            "model": "analytics.fact_recruitment_funnel",
            "semantic_definitions": "applications; admits; deposits; yield",
            "consumers": "Admissions funnel reporting",
        },
        {
            "product": "census_enrollment",
            "source_entities": "raw.enrollment_census, raw.students, raw.terms, raw.schools, raw.programs",
            "model": "analytics.fact_census_enrollment",
            "semantic_definitions": "census_enrollment; ipeds_enrollment",
            "consumers": "Official census and institutional reporting",
        },
    ]
    _write_csv(OUT_DIR / "lineage_summary.csv", rows)


def export_quality_test_evidence() -> None:
    run_results_path = Path("target/run_results.json")
    if not run_results_path.exists():
        raise SystemExit(
            "target/run_results.json not found — run `dbt build` first so this script "
            "reflects a real, current test run rather than stale or missing evidence."
        )
    data = json.loads(run_results_path.read_text())
    rows = []
    for result in data["results"]:
        unique_id = result["unique_id"]
        if not unique_id.startswith("test."):
            continue
        test_name = unique_id.split(".")[-2] if unique_id.count(".") >= 3 else unique_id
        rows.append(
            {
                "test_name": test_name,
                "result": result["status"],
                "evidence": f"{result['execution_time']:.3f}s, adapter response: {result['adapter_response'].get('_message', result['adapter_response'])}",
            }
        )
    rows.sort(key=lambda r: r["test_name"])
    _write_csv(OUT_DIR / "quality_test_evidence.csv", rows)


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise SystemExit(f"No rows generated for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    export_certification_catalog()
    export_lineage_summary()
    export_quality_test_evidence()
