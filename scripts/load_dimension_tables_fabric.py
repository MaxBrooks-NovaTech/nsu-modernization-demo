# Fabric notebook source
# Load synthetic NSU BI Modernization Demo CSV files into the attached NSU_DEMO Lakehouse.
# Upload the repository's CSV sets beneath the Files area of the attached
# NSU_DEMO Lakehouse before running this notebook:
#   Files/dimension_tables/*.csv
#   Files/mart_tables/*.csv
#   Files/data_governance/*.csv
# Attach NSU_DEMO as the notebook's default Lakehouse. In Fabric notebooks,
# use the relative Lakehouse path Files/... after the default Lakehouse is
# attached. Do not use /lakehouse/default/Files/...; Fabric treats that as an
# invalid OneLake URL in this notebook context. This script does not use SQL
# endpoint credentials.

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

LAKEHOUSE_NAME = "NSU_DEMO"
TARGET_SCHEMA = "dbo"
SOURCE_ROOT = "Files"
DIMENSION_SOURCE_FOLDER = "dimension_tables"
MART_SOURCE_FOLDER = "mart_tables"
GOVERNANCE_SOURCE_FOLDER = "data_governance"
WRITE_MODE = "overwrite"  # CREATE OR REPLACE: replace schema and all rows

school_schema = StructType([
    StructField("school_id", StringType(), False),
    StructField("school_name", StringType(), False),
    StructField("school_code", StringType(), False),
])

program_schema = StructType([
    StructField("program_id", StringType(), False),
    StructField("school_id", StringType(), False),
    StructField("program_name", StringType(), False),
    StructField("degree_level", StringType(), False),
    StructField("cip_code", StringType(), False),
])

term_schema = StructType([
    StructField("term_id", StringType(), False),
    StructField("term_name", StringType(), False),
    StructField("academic_year", StringType(), False),
    StructField("term_start_date", DateType(), False),
    StructField("census_date", DateType(), False),
    StructField("term_end_date", DateType(), False),
])

def source_path(table_name, source_folder):
    path = f"{SOURCE_ROOT}/{source_folder}/{table_name}.csv"
    try:
        exists = notebookutils.fs.exists(path)
    except NameError:
        exists = True
    if not exists:
        raise FileNotFoundError(
            f"Missing Lakehouse file: {path}. Attach NSU_DEMO as the default "
            f"Lakehouse and upload {table_name}.csv to Files/{source_folder}/."
        )
    return path

def load_csv_table(table_name, schema, source_folder, key_column=None):
    # Read, type-cast, validate, and replace one Lakehouse table.
    path = source_path(table_name, source_folder)
    spark_table_name = table_name
    endpoint_table_name = f"{TARGET_SCHEMA}.{table_name}"

    raw = (
        spark.read
        .option("header", True)
        .option("mode", "FAILFAST")
        .option("enforceSchema", True)
        .csv(path)
    )
    expected = [field.name for field in schema.fields]
    if raw.columns != expected:
        raise ValueError(f"{table_name}: expected columns {expected}, found {raw.columns}")

    # Read CSV values as text first, then explicitly cast. This handles the
    # PostgreSQL-style t/f boolean values present in the exported CSVs.
    import pyspark.sql.functions as F
    typed_columns = []
    for field in schema.fields:
        source = F.col(field.name)
        if isinstance(field.dataType, DateType):
            typed = F.to_date(source, "yyyy-MM-dd")
        elif isinstance(field.dataType, BooleanType):
            value = F.lower(F.trim(source))
            typed = (
                F.when(value.isin("true", "t", "1"), F.lit(True))
                .when(value.isin("false", "f", "0"), F.lit(False))
                .otherwise(F.lit(None).cast(BooleanType()))
            )
        else:
            typed = source.cast(field.dataType)
        typed_columns.append(typed.alias(field.name))
    df = raw.select(*typed_columns)

    for field in schema.fields:
        if not field.nullable and df.filter(F.col(field.name).isNull()).limit(1).count() > 0:
            raise ValueError(f"{table_name}: null or invalid value in required column {field.name}")

    key_column = key_column or schema.fields[0].name
    if key_column and df.groupBy(key_column).count().filter("count > 1").limit(1).count():
        raise ValueError(f"{table_name}: duplicate values found in key column {key_column}")

    # CREATE OR REPLACE equivalent: replace both the schema and all rows.
    df.write.format("delta").mode(WRITE_MODE).option("overwriteSchema", "true").saveAsTable(spark_table_name)
    return endpoint_table_name, df.count()

fact_enrollment_schema = StructType([
    StructField("registration_id", StringType(), False), StructField("student_id", StringType(), False),
    StructField("section_id", StringType(), False), StructField("term_id", StringType(), False),
    StructField("school_id", StringType(), False), StructField("program_id", StringType(), False),
    StructField("course_code", StringType(), False), StructField("section_number", StringType(), False),
    StructField("registration_date", DateType(), False), StructField("registration_status", StringType(), False),
    StructField("credit_hours", DecimalType(10, 2), False), StructField("grade_mode", StringType(), False),
    StructField("student_type", StringType(), False), StructField("residency_status", StringType(), False),
    StructField("admit_school_id", StringType(), False), StructField("admit_program_id", StringType(), False),
    StructField("modality", StringType(), False), StructField("capacity", IntegerType(), False),
])

recruitment_funnel_schema = StructType([
    StructField("application_id", StringType(), False), StructField("student_id", StringType(), False),
    StructField("term_id", StringType(), False), StructField("school_id", StringType(), False),
    StructField("program_id", StringType(), False), StructField("application_date", DateType(), False),
    StructField("application_status", StringType(), False), StructField("admission_id", StringType(), True),
    StructField("decision_date", DateType(), True), StructField("decision_status", StringType(), True),
    StructField("deposit_id", StringType(), True), StructField("deposit_date", DateType(), True),
    StructField("deposit_status", StringType(), True), StructField("deposit_amount", DecimalType(12, 2), True),
    StructField("is_admitted", BooleanType(), False), StructField("is_deposited", BooleanType(), False),
])

census_enrollment_schema = StructType([
    StructField("enrollment_id", StringType(), False), StructField("student_id", StringType(), False),
    StructField("term_id", StringType(), False), StructField("school_id", StringType(), False),
    StructField("program_id", StringType(), False), StructField("census_enrolled_flag", BooleanType(), False),
    StructField("ipeds_enrolled_flag", BooleanType(), False), StructField("total_credit_hours", DecimalType(10, 2), False),
    StructField("enrollment_status", StringType(), False),
])

mart_specs = [
    ("fact_enrollment", fact_enrollment_schema),
    ("fact_recruitment_funnel", recruitment_funnel_schema),
    ("fact_census_enrollment", census_enrollment_schema),
]

governance_specs = [
    ("certification_catalog", StructType([
        StructField("product", StringType(), False), StructField("model", StringType(), False),
        StructField("version", StringType(), False), StructField("owner", StringType(), False),
        StructField("steward", StringType(), False), StructField("status", StringType(), False),
        StructField("last_reviewed", StringType(), False), StructField("approver_role", StringType(), False),
        StructField("approval_decision", StringType(), False), StructField("consumers", StringType(), False),
        StructField("semantic_definitions", StringType(), False),
    ])),
    ("lineage_summary", StructType([
        StructField("product", StringType(), False), StructField("source_entities", StringType(), False),
        StructField("model", StringType(), False), StructField("semantic_definitions", StringType(), False),
        StructField("consumers", StringType(), False),
    ])),
    ("quality_test_evidence", StructType([
        StructField("test_name", StringType(), False), StructField("result", StringType(), False),
        StructField("evidence", StringType(), False),
    ])),
]

# Preflight every source before replacing any table.
source_specs = [
    ("dim_school", school_schema, DIMENSION_SOURCE_FOLDER),
    ("dim_program", program_schema, DIMENSION_SOURCE_FOLDER),
    ("dim_term", term_schema, DIMENSION_SOURCE_FOLDER),
]
source_specs.extend((table_name, schema, MART_SOURCE_FOLDER) for table_name, schema in mart_specs)
source_specs.extend((table_name, schema, GOVERNANCE_SOURCE_FOLDER) for table_name, schema in governance_specs)
for table_name, _, folder in source_specs:
    print(f"Found source: {source_path(table_name, folder)}")

results = [
    load_csv_table("dim_school", school_schema, DIMENSION_SOURCE_FOLDER),
    load_csv_table("dim_program", program_schema, DIMENSION_SOURCE_FOLDER),
    load_csv_table("dim_term", term_schema, DIMENSION_SOURCE_FOLDER),
]
results.extend(load_csv_table(table_name, schema, MART_SOURCE_FOLDER) for table_name, schema in mart_specs)

results.extend(load_csv_table(table_name, schema, GOVERNANCE_SOURCE_FOLDER) for table_name, schema in governance_specs)

for table_name, row_count in results:
    print(f"Created and loaded {row_count} rows into {table_name}")
# Validation cell. Spark uses the unqualified table name; the SQL analytics
# endpoint exposes the same managed table in schema dbo. Every table above has
# already been replaced with its explicit schema and CSV contents.

expected_counts = {
    "dim_school": 12,
    "dim_program": 36,
    "dim_term": 6,
    "fact_enrollment": 2148,
    "fact_recruitment_funnel": 300,
    "fact_census_enrollment": 1074,
    "certification_catalog": 3,
    "lineage_summary": 3,
    "quality_test_evidence": 47,
}

for table_name, expected in expected_counts.items():
    actual = spark.table(table_name).count()
    if actual != expected:
        raise ValueError(f"{table_name}: expected {expected} rows, found {actual}")
    print(f"Validation passed: {TARGET_SCHEMA}.{table_name} has {actual} rows")

# Optional SQL endpoint validation after the notebook completes:
# SELECT TABLE_SCHEMA, TABLE_NAME
# FROM INFORMATION_SCHEMA.TABLES
# WHERE TABLE_SCHEMA = 'dbo'
#   AND TABLE_NAME IN (
#       'dim_school', 'dim_program', 'dim_term',
#       'fact_enrollment', 'fact_recruitment_funnel', 'fact_census_enrollment',
#       'certification_catalog', 'lineage_summary', 'quality_test_evidence'
#   );
