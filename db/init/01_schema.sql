CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.budget_actuals CASCADE;
DROP TABLE IF EXISTS raw.enrollment_census CASCADE;
DROP TABLE IF EXISTS raw.registrations CASCADE;
DROP TABLE IF EXISTS raw.deposits CASCADE;
DROP TABLE IF EXISTS raw.admissions CASCADE;
DROP TABLE IF EXISTS raw.applications CASCADE;
DROP TABLE IF EXISTS raw.course_sections CASCADE;
DROP TABLE IF EXISTS raw.terms CASCADE;
DROP TABLE IF EXISTS raw.students CASCADE;
DROP TABLE IF EXISTS raw.programs CASCADE;
DROP TABLE IF EXISTS raw.schools CASCADE;

CREATE TABLE raw.schools (
    school_id text PRIMARY KEY,
    school_name text NOT NULL,
    school_code text NOT NULL UNIQUE,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.programs (
    program_id text PRIMARY KEY,
    school_id text NOT NULL REFERENCES raw.schools (school_id),
    program_name text NOT NULL,
    degree_level text NOT NULL,
    cip_code text NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.terms (
    term_id text PRIMARY KEY,
    term_name text NOT NULL,
    academic_year text NOT NULL,
    term_start_date date NOT NULL,
    census_date date NOT NULL,
    term_end_date date NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.students (
    student_id text PRIMARY KEY,
    student_type text NOT NULL,
    residency_status text NOT NULL,
    entry_term_id text NOT NULL REFERENCES raw.terms (term_id),
    admit_school_id text NOT NULL REFERENCES raw.schools (school_id),
    admit_program_id text NOT NULL REFERENCES raw.programs (program_id),
    synthetic_birth_year integer NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.course_sections (
    section_id text PRIMARY KEY,
    term_id text NOT NULL REFERENCES raw.terms (term_id),
    school_id text NOT NULL REFERENCES raw.schools (school_id),
    program_id text NOT NULL REFERENCES raw.programs (program_id),
    course_code text NOT NULL,
    section_number text NOT NULL,
    modality text NOT NULL,
    capacity integer NOT NULL,
    UNIQUE (term_id, program_id, course_code, section_number),
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.applications (
    application_id text PRIMARY KEY,
    student_id text NOT NULL REFERENCES raw.students (student_id),
    term_id text NOT NULL REFERENCES raw.terms (term_id),
    school_id text NOT NULL REFERENCES raw.schools (school_id),
    program_id text NOT NULL REFERENCES raw.programs (program_id),
    application_date date NOT NULL,
    application_status text NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.admissions (
    admission_id text PRIMARY KEY,
    application_id text NOT NULL UNIQUE REFERENCES raw.applications (application_id),
    decision_date date NOT NULL,
    decision_status text NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.deposits (
    deposit_id text PRIMARY KEY,
    admission_id text NOT NULL UNIQUE REFERENCES raw.admissions (admission_id),
    deposit_date date NOT NULL,
    deposit_status text NOT NULL,
    deposit_amount numeric(10, 2) NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.registrations (
    registration_id text PRIMARY KEY,
    student_id text NOT NULL REFERENCES raw.students (student_id),
    section_id text NOT NULL REFERENCES raw.course_sections (section_id),
    term_id text NOT NULL REFERENCES raw.terms (term_id),
    registration_date date NOT NULL,
    registration_status text NOT NULL,
    credit_hours numeric(4, 1) NOT NULL,
    grade_mode text NOT NULL,
    UNIQUE (student_id, section_id, term_id),
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.enrollment_census (
    enrollment_id text PRIMARY KEY,
    student_id text NOT NULL REFERENCES raw.students (student_id),
    term_id text NOT NULL REFERENCES raw.terms (term_id),
    school_id text NOT NULL REFERENCES raw.schools (school_id),
    program_id text NOT NULL REFERENCES raw.programs (program_id),
    census_enrolled_flag boolean NOT NULL,
    ipeds_enrolled_flag boolean NOT NULL,
    total_credit_hours numeric(5, 1) NOT NULL,
    enrollment_status text NOT NULL,
    UNIQUE (student_id, term_id),
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE raw.budget_actuals (
    budget_actual_id text PRIMARY KEY,
    fiscal_year text NOT NULL,
    school_id text NOT NULL REFERENCES raw.schools (school_id),
    revenue_budget numeric(12, 2) NOT NULL,
    revenue_actual numeric(12, 2) NOT NULL,
    expense_budget numeric(12, 2) NOT NULL,
    expense_actual numeric(12, 2) NOT NULL,
    UNIQUE (fiscal_year, school_id),
    loaded_at timestamptz NOT NULL DEFAULT now()
);
