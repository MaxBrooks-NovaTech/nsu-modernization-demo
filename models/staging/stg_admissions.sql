select
    admission_id,
    application_id,
    decision_date,
    decision_status
from {{ source('raw', 'admissions') }}