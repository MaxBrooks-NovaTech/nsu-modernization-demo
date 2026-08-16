select
    student_id,
    section_id,
    term_id,
    count(*) as row_count
from {{ ref('fact_enrollment') }}
group by student_id, section_id, term_id
having count(*) <> 1