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
1. Upload the files using the folder layout above.

### Attach `NSU_DEMO` as the default Lakehouse
1. Open the Fabric workspace containing `NSU_DEMO`.
2. Open an existing notebook or select **New > Notebook**.
3. In the notebook toolbar, locate the **Lakehouse** pane or **Add lakehouse** control. If the pane is hidden, open it from the notebook's left-side explorer or **View** menu.
4. Select **Add lakehouse**.
5. Choose **Existing lakehouse**.
6. Search for `NSU_DEMO`.
7. Select the Lakehouse named `NSU_DEMO` in the correct workspace and choose **Add**.
8. In the attached Lakehouse list, open the `...` menu for `NSU_DEMO` and choose **Set as default** if it is not already marked as the default Lakehouse.
9. Confirm the notebook Lakehouse pane shows `NSU_DEMO` with `Tables` and `Files` beneath it. The default attachment is required because the script reads relative paths such as `Files/dimension_tables/dim_school.csv`.
10. If the notebook was already open while the Lakehouse was attached, restart the notebook session or refresh the Lakehouse pane before running the script.

2. Confirm the files are visible under the Lakehouse `Files` area. The script uses the relative path `Files/...` after the default Lakehouse is attached. Do not change it to `/lakehouse/default/Files/...`; that path can produce an `IllegalArgumentException` in Fabric notebook Spark reads.
3. Copy `scripts/load_dimension_tables_fabric.py` into notebook cells, or upload/import it if supported.
4. Run all cells.
5. Confirm the row-count validation output.
6. Validate the resulting tables through the SQL endpoint using `dbo.<table_name>`, for example `dbo.dim_school` and `dbo.fact_enrollment`.

## Missing-file error
If the notebook reports an error containing a path such as `.../lakehouse/default/Files/dimension_tables/dim_school.csv`, verify:

- `NSU_DEMO` is attached as the notebook's default Lakehouse, not only added as an additional Lakehouse.
- The script uses `SOURCE_ROOT = "Files"`, not `/lakehouse/default/Files`.
- The file is named exactly `dim_school.csv`.
- The file is directly under `Files/dimension_tables/`, not under an additional nested folder.
- The file upload has completed and the Lakehouse Files view has been refreshed.

The loader prints the expected source paths and lets the first Spark CSV read validate that each file exists and is readable. It intentionally does not call `notebookutils.fs.exists()` because some Fabric runtimes resolve relative paths through `/user/trusted-service-user/Files` and return a misleading OneLake HTTP 400.

The loader performs `CREATE OR REPLACE` behavior for every managed Delta table. It applies the explicit schema and overwrites the complete table contents from the CSV in one operation. Rerunning it after deleting and re-uploading source files replaces every fact, dimension, and governance table deterministically. Spark writes managed tables without a namespace, and the Lakehouse SQL analytics endpoint exposes them under the `dbo` schema as `dbo.<table_name>`. It validates non-null required columns, duplicate primary keys, explicit data types, and expected row counts. Optional nullable columns in the fact tables are allowed to contain nulls. Governance CSVs are loaded as separate reference tables from `Files/data_governance/`.

The SQL endpoint connection string is not needed by the notebook. Do not place credentials, tokens, or connection strings in the notebook or repository.
