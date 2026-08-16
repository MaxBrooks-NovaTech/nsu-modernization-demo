-- Fails (returns a row) if FactEnrollment falls below the contract's minimum_row_count of 1.
-- See contracts/fact_enrollment.yml: quality.minimum_row_count.
select count(*) as row_count
from {{ ref('fact_enrollment') }}
having count(*) < 1
