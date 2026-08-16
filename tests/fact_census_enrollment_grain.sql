select student_id, term_id
from {{ ref('fact_census_enrollment') }}
group by student_id, term_id
having count(*) > 1