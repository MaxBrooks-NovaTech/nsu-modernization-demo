select
    enrollment_id,
    student_id,
    term_id,
    school_id,
    program_id,
    census_enrolled_flag,
    ipeds_enrolled_flag,
    total_credit_hours,
    enrollment_status
from {{ ref('stg_enrollment_census') }}