# Fabric Lakehouse CSV Loader

Use `load_dimension_tables_fabric.py` in a Microsoft Fabric notebook attached to the `NSU_DEMO` Lakehouse. Despite its historical filename, the loader now imports both dimension and mart CSV sets.

## Lakehouse Files layout

Upload the CSV files into these folders in the attached Lakehouse:

```text
Files/
├── dimension_tables/
│   ├── dim_school.csv
│   ├── dim_program.csv
│   └── dim_term.csv
├── mart_tables/
│   ├── fact_enrollment.csv
│   ├── fact_recruitment_funnel.csv
│   └── fact_census_enrollment.csv
└── data_governance/
    ├── certification_catalog.csv
    ├── lineage_summary.csv
    └── quality_test_evidence.csv
```

The source files are generated locally under `seeds/dimension_tables/`, `seeds/mart_tables/`, and `data_governance/`. Upload the contents of each local folder to the corresponding Lakehouse `Files/` folder. The governance files must be placed in `Files/data_governance/`, separate from the mart files.

## Tables loaded

| Lakehouse table | Source folder/file | Expected rows |
| --- | --- | ---: |
| `dim_school` | `Files/dimension_tables/dim_school.csv` | 12 |
| `dim_program` | `Files/dimension_tables/dim_program.csv` | 36 |
| `dim_term` | `Files/dimension_tables/dim_term.csv` | 6 |
| `fact_enrollment` | `Files/mart_tables/fact_enrollment.csv` | 2,148 |
| `fact_recruitment_funnel` | `Files/mart_tables/fact_recruitment_funnel.csv` | 300 |
| `fact_census_enrollment` | `Files/mart_tables/fact_census_enrollment.csv` | 1,074 |
| `certification_catalog` | `Files/data_governance/certification_catalog.csv` | 3 |
| `lineage_summary` | `Files/data_governance/lineage_summary.csv` | 3 |
| `quality_test_evidence` | `Files/data_governance/quality_test_evidence.csv` | 47 |

## Steps

1. 1. Upload the files using the folder layout above.
2. Open a Fabric notebook and attach `NSU_DEMO` as the **default Lakehouse**. The notebook must show `NSU_DEMO` in its Lakehouse pane.
3. Confirm the files are visible under the Lakehouse `Files` area. The script uses `/lakehouse/default/Files/...`, not the relative path `Files/...`.
4. Copy `scripts/load_dimension_tables_fabric.py` into notebook cells, or upload/import it if supported.
5. Run all cells.
5. Confirm the row-count validation output.
6. Validate the resulting tables through the SQL endpoint using `dbo.<table_name>`, for example `dbo.dim_school` and `dbo.fact_enrollment`.

## Missing-file error
If the notebook reports an error containing a path such as `.../Files/dimension_tables/dim_school.csv`, verify:

- `NSU_DEMO` is attached as the notebook's default Lakehouse, not only added as an additional Lakehouse.
- The file is named exactly `dim_school.csv`.
- The file is directly under `Files/dimension_tables/`, not under an additional nested folder.
- The file upload has completed and the Lakehouse Files view has been refreshed.

The loader performs a preflight existence check before replacing any tables and reports the expected absolute Lakehouse path for a missing file.

The loader performs `CREATE OR REPLACE` behavior for every managed Delta table. It applies the explicit schema and overwrites the complete table contents from the CSV in one operation. Rerunning it after deleting and re-uploading source files replaces every fact, dimension, and governance table deterministically. Spark writes managed tables without a namespace, and the Lakehouse SQL analytics endpoint exposes them under the `dbo` schema as `dbo.<table_name>`. It validates non-null required columns, duplicate primary keys, explicit data types, and expected row counts. Optional nullable columns in the fact tables are allowed to contain nulls. Governance CSVs are loaded as separate reference tables from `Files/data_governance/`.

The SQL endpoint connection string is not needed by the notebook. Do not place credentials, tokens, or connection strings in the notebook or repository.
