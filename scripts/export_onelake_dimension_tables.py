#!/usr/bin/env python3
"Export Power BI slicer dimensions as OneLake-ready CSV snapshots."""

from __future__ import annotations
import csv
from pathlib import Path
SOURCE_DIR = Path("seeds")
OUT_DIR = Path("seeds/dimension_tables")

DIMENSIONS = {
    "dim_school.csv": ("schools.csv", "school_id"),
    "dim_program.csv": ("programs.csv", "program_id"),
    "dim_term.csv": ("terms.csv", "term_id"),
}


def export_dimension(output_name: str, source_name: str, key: str) -> int:
    source_path = SOURCE_DIR / source_name
    output_path = OUT_DIR / output_name
    with source_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        if not reader.fieldnames or key not in reader.fieldnames:
            raise ValueError(f"{source_path} is missing required key {key!r}")
    keys = [row[key] for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{source_path} contains duplicate {key} values")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=reader.fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output_path}")
    return len(rows)


def main() -> None:
    total = sum(export_dimension(out, source, key) for out, (source, key) in DIMENSIONS.items())
    print(f"Exported {len(DIMENSIONS)} OneLake dimension tables and {total} rows.")

if __name__ == "__main__":
    main()
