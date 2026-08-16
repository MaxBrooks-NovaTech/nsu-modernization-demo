select *
from {{ ref('fact_enrollment') }}
where credit_hours < 0
   or (registration_status = 'Dropped' and credit_hours <> 0)
   or (registration_status in ('Registered', 'Withdrawn') and credit_hours <= 0)