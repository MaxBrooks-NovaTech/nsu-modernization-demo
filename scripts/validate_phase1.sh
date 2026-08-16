#!/usr/bin/env bash
set -euo pipefail

docker compose exec -T postgres psql -U "${POSTGRES_USER:-nsu_demo_user}" -d "${POSTGRES_DB:-nsu_modernization_demo}" -v ON_ERROR_STOP=1 <<'SQL'
SELECT 'schools' AS table_name, COUNT(*) AS row_count FROM raw.schools
UNION ALL SELECT 'programs', COUNT(*) FROM raw.programs
UNION ALL SELECT 'students', COUNT(*) FROM raw.students
UNION ALL SELECT 'terms', COUNT(*) FROM raw.terms
UNION ALL SELECT 'course_sections', COUNT(*) FROM raw.course_sections
UNION ALL SELECT 'applications', COUNT(*) FROM raw.applications
UNION ALL SELECT 'admissions', COUNT(*) FROM raw.admissions
UNION ALL SELECT 'deposits', COUNT(*) FROM raw.deposits
UNION ALL SELECT 'registrations', COUNT(*) FROM raw.registrations
UNION ALL SELECT 'enrollment_census', COUNT(*) FROM raw.enrollment_census
UNION ALL SELECT 'budget_actuals', COUNT(*) FROM raw.budget_actuals
ORDER BY table_name;

DO $validate$
DECLARE
    expected_counts jsonb := '{"schools":12,"programs":36,"students":240,"terms":6,"course_sections":432,"applications":300,"admissions":201,"deposits":109,"registrations":2148,"enrollment_census":1074,"budget_actuals":24}'::jsonb;
    table_name text;
    expected_count integer;
    actual_count integer;
BEGIN
    FOR table_name, expected_count IN
        SELECT key, value::integer FROM jsonb_each_text(expected_counts)
    LOOP
        EXECUTE format('SELECT COUNT(*) FROM raw.%I', table_name) INTO actual_count;
        IF actual_count <> expected_count THEN
            RAISE EXCEPTION 'Expected % rows in raw.%, found %', expected_count, table_name, actual_count;
        END IF;
    END LOOP;

    IF EXISTS (
        SELECT 1 FROM raw.students st
        LEFT JOIN raw.terms t ON t.term_id = st.entry_term_id
        WHERE t.term_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Student entry-term referential integrity failed';
    END IF;

    IF EXISTS (
        SELECT 1 FROM raw.admissions a
        LEFT JOIN raw.applications ap ON ap.application_id = a.application_id
        WHERE ap.application_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Admission application referential integrity failed';
    END IF;

    IF EXISTS (
        SELECT 1 FROM raw.deposits d
        LEFT JOIN raw.admissions a ON a.admission_id = d.admission_id
        WHERE a.admission_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Deposit admission referential integrity failed';
    END IF;

    IF EXISTS (
        SELECT 1 FROM raw.programs p
        LEFT JOIN raw.schools s ON s.school_id = p.school_id
        WHERE s.school_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Program school referential integrity failed';
    END IF;

    IF EXISTS (
        SELECT student_id, section_id, term_id
        FROM raw.registrations
        GROUP BY student_id, section_id, term_id
        HAVING COUNT(*) > 1
    ) THEN
        RAISE EXCEPTION 'Duplicate registration grain found';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM raw.enrollment_census e
        LEFT JOIN raw.students st ON st.student_id = e.student_id
        LEFT JOIN raw.terms t ON t.term_id = e.term_id
        LEFT JOIN raw.schools s ON s.school_id = e.school_id
        LEFT JOIN raw.programs p ON p.program_id = e.program_id
        WHERE st.student_id IS NULL
           OR t.term_id IS NULL
           OR s.school_id IS NULL
           OR p.program_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Enrollment referential integrity failed';
    END IF;
END $validate$;
SQL
