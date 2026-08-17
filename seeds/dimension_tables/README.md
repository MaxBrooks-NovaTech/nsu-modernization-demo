# OneLake Dimension Tables

These CSV snapshots support the Power BI dashboard slicers described in `PowerBIDashboard.md` and are intended for upload to a OneLake Lakehouse as dimension tables.

## Files

| File | Grain | Key | Rows | Purpose |
| ----------------- | ---------------------------- | ------------ | ---: | ------------------------------------------ |
| `dim_school.csv` | One row per school | `school_id` | 12 | School slicers and school-level chart axes |
| `dim_program.csv` | One row per academic program | `program_id` | 36 | Program slicers and program analysis |
| `dim_term.csv` | One row per academic term | `term_id` | 6 | Term slicers and academic-period filtering |

The source data is deterministic and synthetic. These files are copied from the authoritative source snapshots in `seeds/schools.csv`, `seeds/programs.csv`, and `seeds/terms.csv` by:

```bash
python3 scripts/export_onelake_dimension_tables.py
```

## OneLake upload guidance

Upload each CSV as a separate Lakehouse table using the filename without `.csv` as the table name, or retain the `dim_` prefix for explicit dimensional modeling. Preserve the key columns and use them for many-to-one relationships from the fact tables:

- `FactEnrollment`, `RecruitmentFunnel`, and `CensusEnrollment` `school_id` -> `dim_school.school_id`
- `FactEnrollment`, `RecruitmentFunnel`, and `CensusEnrollment` `program_id` -> `dim_program.program_id`
- `FactEnrollment`, `RecruitmentFunnel`, and `CensusEnrollment` `term_id` -> `dim_term.term_id`

This is a synthetic demonstration dataset. It is not connected to NSU production systems and must not be replaced with real student or institutional data without separate governance authorization.
