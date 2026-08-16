select
    section_id,
    term_id,
    school_id,
    program_id,
    course_code,
    section_number,
    modality,
    capacity
from {{ source('raw', 'course_sections') }}