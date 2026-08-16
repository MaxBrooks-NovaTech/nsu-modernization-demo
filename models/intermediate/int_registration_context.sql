select
    r.registration_id,
    r.student_id,
    r.section_id,
    r.term_id,
    r.registration_date,
    r.registration_status,
    r.credit_hours,
    r.grade_mode,
    s.student_type,
    s.residency_status,
    s.admit_school_id,
    s.admit_program_id,
    cs.school_id,
    cs.program_id,
    cs.course_code,
    cs.section_number,
    cs.modality,
    cs.capacity
from {{ ref('stg_registrations') }} r
join {{ ref('stg_students') }} s on s.student_id = r.student_id
join {{ ref('stg_course_sections') }} cs
  on cs.section_id = r.section_id
 and cs.term_id = r.term_id