#!/usr/bin/env python3
"""Detect breaking and non-breaking changes between two FactEnrollment contract YAML files."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
import yaml


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def extract_contract(data: dict) -> dict:
    """Extract contract dictionary whether defined at root or under a 'contract' key."""
    if "contract" in data and isinstance(data["contract"], dict):
        return data["contract"]
    return data


def compare_metrics(old_metrics: dict, new_metrics: dict) -> list[str]:
    """Compare semantic metric definitions (semantic/metric_definitions.yml style)."""
    changes: list[str] = []
    old_names = set(old_metrics or {})
    new_names = set(new_metrics or {})

    for name in sorted(old_names - new_names):
        changes.append(f"breaking: certified metric removed: {name}")
    for name in sorted(new_names - old_names):
        changes.append(f"info: new metric added: {name}")

    for name in sorted(old_names & new_names):
        old_metric = old_metrics[name] or {}
        new_metric = new_metrics[name] or {}
        was_certified = old_metric.get("certification_status") == "Certified"

        if was_certified and old_metric.get("calculation") != new_metric.get("calculation"):
            changes.append(f"breaking: certified metric calculation changed: {name}")
        if was_certified and old_metric.get("grain") != new_metric.get("grain"):
            changes.append(f"breaking: certified metric grain changed: {name}")

        old_status = old_metric.get("certification_status")
        new_status = new_metric.get("certification_status")
        if old_status != new_status:
            if was_certified:
                changes.append(
                    f"breaking: certified metric status changed: {name} ('{old_status}' -> '{new_status}')"
                )
            else:
                changes.append(
                    f"info: metric certification status changed: {name} ('{old_status}' -> '{new_status}')"
                )

        if old_metric.get("definition") != new_metric.get("definition"):
            changes.append(f"info: metric description changed: {name}")

    return changes


def compare(before: dict, after: dict) -> list[str]:
    changes: list[str] = []
    old = extract_contract(before)
    new = extract_contract(after)

    # 0. Semantic metric definition documents (e.g. semantic/metric_definitions.yml)
    if "metrics" in old or "metrics" in new:
        return compare_metrics(old.get("metrics", {}), new.get("metrics", {}))

    # 1. Required fields comparison
    old_fields = set(old.get("required_fields", []) or [])
    new_fields = set(new.get("required_fields", []) or [])
    for name in sorted(old_fields - new_fields):
        changes.append(f"breaking: required field removed: {name}")
    for name in sorted(new_fields - old_fields):
        changes.append(f"info: optional/new field added: {name}")

    # 2. Grain comparison
    old_grain = old.get("grain")
    new_grain = new.get("grain")
    if old_grain and new_grain and old_grain != new_grain:
        changes.append(f"breaking: contract grain changed from '{old_grain}' to '{new_grain}'")
    elif old_grain != new_grain:
        changes.append("breaking: contract grain changed")

    # 3. Quality required tests comparison
    old_quality = old.get("quality", {})
    new_quality = new.get("quality", {})
    if isinstance(old_quality, dict) and isinstance(new_quality, dict):
        old_tests = set(old_quality.get("required_tests", []) or [])
        new_tests = set(new_quality.get("required_tests", []) or [])
        for test in sorted(old_tests - new_tests):
            changes.append(f"breaking: required quality test removed: {test}")

    # 4. Certification status comparison
    old_status = old.get("status")
    new_status = new.get("status")
    if old_status == "Certified" and new_status != "Certified":
        changes.append(
            f"breaking: certification status changed from '{old_status}' to '{new_status}'"
        )

    # 5. Breaking change rules comparison
    old_rules = old.get("breaking_change_rules", []) or []
    new_rules = new.get("breaking_change_rules", []) or []
    if old_rules != new_rules:
        changes.append("breaking: contract breaking-change rules changed")

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Check contract changes between two versions.")
    parser.add_argument("before", type=Path, help="Path to base contract YAML")
    parser.add_argument("after", type=Path, help="Path to target contract YAML")
    args = parser.parse_args()

    changes = compare(load(args.before), load(args.after))
    if changes:
        print("\n".join(changes))
        has_breaking = any(c.startswith("breaking:") for c in changes)
        return 1 if has_breaking else 0

    print("No breaking contract changes detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

