select
    application_id,
    student_id,
    term_id,
    school_id,
    program_id,
    application_date,
    application_status
from {{ source('raw', 'applications') }}