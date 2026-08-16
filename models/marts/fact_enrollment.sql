{{ config(materialized='table', alias='FactEnrollment') }}

select
    registration_id,
    student_id,
    section_id,
    term_id,
    school_id,
    program_id,
    course_code,
    section_number,
    registration_date,
    registration_status,
    credit_hours,
    grade_mode,
    student_type,
    residency_status,
    admit_school_id,
    admit_program_id,
    modality,
    capacity
from {{ ref('int_registration_context') }}
