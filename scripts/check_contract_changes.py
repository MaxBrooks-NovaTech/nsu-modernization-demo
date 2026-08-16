#!/usr/bin/env python3
"Detect breaking changes between two FactEnrollment contract YAML files."

from __future__ import annotations
import argparse
import sys
from pathlib import Path
import yaml


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def compare(before: dict, after: dict) -> list[str]:
    changes: list[str] = []
    old = before.get("contract", {})
    new = after.get("contract", {})
    old_fields = set(old.get("required_fields", []))
    new_fields = set(new.get("required_fields", []))
    for name in sorted(old_fields - new_fields):
        changes.append(f"breaking: required field removed: {name}")
    old_grain = old.get("grain")
    new_grain = new.get("grain")
    if old_grain != new_grain:
        changes.append("breaking: contract grain changed")
    old_rules = old.get("breaking_change_rules", [])
    new_rules = new.get("breaking_change_rules", [])
    if old_rules != new_rules:
        changes.append("breaking: contract breaking-change rules changed")
    return changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    changes = compare(load(args.before), load(args.after))
    if changes:
        print("\\n".join(changes))
        return 1
    print("No breaking contract changes detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
