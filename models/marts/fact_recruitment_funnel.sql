with applications as (
    select * from {{ ref('stg_applications') }}
),
admissions as (
    select * from {{ ref('stg_admissions') }}
),
deposits as (
    select * from {{ ref('stg_deposits') }}
)
select
    a.application_id,
    a.student_id,
    a.term_id,
    a.school_id,
    a.program_id,
    a.application_date,
    a.application_status,
    adm.admission_id,
    adm.decision_date,
    adm.decision_status,
    dep.deposit_id,
    dep.deposit_date,
    dep.deposit_status,
    dep.deposit_amount,
    (adm.admission_id is not null) as is_admitted,
    (dep.deposit_id is not null and dep.deposit_status = 'Paid') as is_deposited
from applications a
left join admissions adm on a.application_id = adm.application_id
left join deposits dep on adm.admission_id = dep.admission_id