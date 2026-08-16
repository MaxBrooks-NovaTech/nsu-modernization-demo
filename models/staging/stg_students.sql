select
    student_id,
    student_type,
    residency_status,
    entry_term_id,
    admit_school_id,
    admit_program_id,
    synthetic_birth_year
from {{ source('raw', 'students') }}