select
    registration_id,
    student_id,
    section_id,
    term_id,
    registration_date,
    registration_status,
    credit_hours,
    grade_mode
from {{ source('raw', 'registrations') }}