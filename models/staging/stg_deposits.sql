select
    deposit_id,
    admission_id,
    deposit_date,
    deposit_status,
    deposit_amount
from {{ source('raw', 'deposits') }}