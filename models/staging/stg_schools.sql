select school_id, school_name, school_code
from {{ source('raw', 'schools') }}