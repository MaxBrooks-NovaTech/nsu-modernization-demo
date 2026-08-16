select program_id, school_id, program_name, degree_level, cip_code
from {{ source('raw', 'programs') }}