select
    term_id,
    term_name,
    academic_year,
    term_start_date,
    census_date,
    term_end_date
from {{ source('raw', 'terms') }}