#!/usr/bin/env python3
"""Generate deterministic synthetic source data for the Phase 1 demo."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


SEED = 20260816
OUTPUT_DIR = Path("seeds")

SCHOOLS = [
    ("SCH01", "College of Arts and Sciences", "CAS"),
    ("SCH02", "College of Business and Analytics", "CBA"),
    ("SCH03", "College of Computing and Engineering", "CCE"),
    ("SCH04", "College of Education", "COE"),
    ("SCH05", "College of Health Professions", "CHP"),
    ("SCH06", "College of Nursing", "CON"),
    ("SCH07", "College of Psychology", "CPS"),
    ("SCH08", "College of Public Policy", "CPP"),
    ("SCH09", "College of Law", "LAW"),
    ("SCH10", "College of Medicine", "MED"),
    ("SCH11", "College of Pharmacy", "PHR"),
    ("SCH12", "College of Ocean and Environment", "OCE"),
]

DEGREE_LEVELS = ["Bachelors", "Masters", "Doctoral"]
PROGRAM_SUFFIXES = ["Studies", "Leadership", "Applied Science"]
TERMS = [
    ("2024FA", "Fall 2024", "2024-2025", date(2024, 8, 19), date(2024, 9, 9), date(2024, 12, 13)),
    ("2025WI", "Winter 2025", "2024-2025", date(2025, 1, 6), date(2025, 1, 27), date(2025, 4, 25)),
    ("2025SU", "Summer 2025", "2024-2025", date(2025, 5, 5), date(2025, 5, 26), date(2025, 8, 8)),
    ("2025FA", "Fall 2025", "2025-2026", date(2025, 8, 18), date(2025, 9, 8), date(2025, 12, 12)),
    ("2026WI", "Winter 2026", "2025-2026", date(2026, 1, 5), date(2026, 1, 26), date(2026, 4, 24)),
    ("2026SU", "Summer 2026", "2025-2026", date(2026, 5, 4), date(2026, 5, 25), date(2026, 8, 7)),
]
MODALITIES = ["In Person", "Hybrid", "Online"]
STUDENT_TYPES = ["First Time", "Transfer", "Continuing", "Graduate"]
RESIDENCIES = ["In State", "Out of State", "International"]
REGISTRATION_STATUSES = ["Registered", "Withdrawn", "Dropped"]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def school_rows() -> list[dict[str, object]]:
    return [
        {"school_id": school_id, "school_name": school_name, "school_code": school_code}
        for school_id, school_name, school_code in SCHOOLS
    ]


def program_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for school_index, (school_id, school_name, _) in enumerate(SCHOOLS, start=1):
        subject = school_name.replace("College of ", "")
        for program_index, degree_level in enumerate(DEGREE_LEVELS, start=1):
            program_id = f"PRG{school_index:02d}{program_index:02d}"
            rows.append(
                {
                    "program_id": program_id,
                    "school_id": school_id,
                    "program_name": f"{subject} {PROGRAM_SUFFIXES[program_index - 1]}",
                    "degree_level": degree_level,
                    "cip_code": f"{school_index:02d}.{program_index:04d}",
                }
            )
    return rows


def term_rows() -> list[dict[str, object]]:
    return [
        {
            "term_id": term_id,
            "term_name": term_name,
            "academic_year": academic_year,
            "term_start_date": start.isoformat(),
            "census_date": census.isoformat(),
            "term_end_date": end.isoformat(),
        }
        for term_id, term_name, academic_year, start, census, end in TERMS
    ]


def student_rows(rng: random.Random, programs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    term_ids = [term[0] for term in TERMS[:4]]
    for index in range(1, 241):
        program = programs[(index - 1) % len(programs)]
        rows.append(
            {
                "student_id": f"STU{index:05d}",
                "student_type": rng.choice(STUDENT_TYPES),
                "residency_status": rng.choice(RESIDENCIES),
                "entry_term_id": rng.choice(term_ids),
                "admit_school_id": program["school_id"],
                "admit_program_id": program["program_id"],
                "synthetic_birth_year": rng.randint(1978, 2008),
            }
        )
    return rows


def section_rows(rng: random.Random, programs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for term_id, *_ in TERMS:
        for program in programs:
            for section_number in range(1, 3):
                sequence = len(rows) + 1
                rows.append(
                    {
                        "section_id": f"SEC{sequence:05d}",
                        "term_id": term_id,
                        "school_id": program["school_id"],
                        "program_id": program["program_id"],
                        "course_code": f"{program['program_id'][-4:]}-{100 + section_number * 50}",
                        "section_number": f"{section_number:02d}",
                        "modality": rng.choice(MODALITIES),
                        "capacity": rng.randint(24, 42),
                    }
                )
    return rows


def application_rows(
    rng: random.Random,
    students: list[dict[str, object]],
    programs: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    applications: list[dict[str, object]] = []
    admissions: list[dict[str, object]] = []
    deposits: list[dict[str, object]] = []
    application_terms = TERMS[1:]
    for index in range(1, 301):
        student = students[(index * 7) % len(students)]
        program = programs[(index * 5) % len(programs)]
        term_id, _, _, start, _, _ = application_terms[index % len(application_terms)]
        application_date = start - timedelta(days=rng.randint(35, 140))
        status = rng.choices(["Submitted", "Cancelled"], weights=[92, 8], k=1)[0]
        application_id = f"APP{index:05d}"
        applications.append(
            {
                "application_id": application_id,
                "student_id": student["student_id"],
                "term_id": term_id,
                "school_id": program["school_id"],
                "program_id": program["program_id"],
                "application_date": application_date.isoformat(),
                "application_status": status,
            }
        )
        if status == "Submitted" and rng.random() < 0.74:
            admission_id = f"ADM{len(admissions) + 1:05d}"
            decision_date = application_date + timedelta(days=rng.randint(10, 45))
            admissions.append(
                {
                    "admission_id": admission_id,
                    "application_id": application_id,
                    "decision_date": decision_date.isoformat(),
                    "decision_status": "Admitted",
                }
            )
            if rng.random() < 0.58:
                deposits.append(
                    {
                        "deposit_id": f"DEP{len(deposits) + 1:05d}",
                        "admission_id": admission_id,
                        "deposit_date": (decision_date + timedelta(days=rng.randint(3, 24))).isoformat(),
                        "deposit_status": "Paid",
                        "deposit_amount": "250.00",
                    }
                )
    return applications, admissions, deposits


def registration_and_enrollment_rows(
    rng: random.Random,
    students: list[dict[str, object]],
    sections: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    sections_by_term_program: dict[tuple[str, str], list[dict[str, object]]] = {}
    for section in sections:
        key = (str(section["term_id"]), str(section["program_id"]))
        sections_by_term_program.setdefault(key, []).append(section)

    registrations: list[dict[str, object]] = []
    enrollment: list[dict[str, object]] = []
    for student in students:
        active_terms = rng.sample([term[0] for term in TERMS], k=rng.randint(3, 6))
        for term_id in sorted(active_terms):
            key = (term_id, str(student["admit_program_id"]))
            available_sections = sections_by_term_program[key]
            selected_sections = rng.sample(available_sections, k=rng.randint(2, min(4, len(available_sections))))
            total_credits = 0.0
            active_registration_count = 0
            school_id = str(student["admit_school_id"])
            program_id = str(student["admit_program_id"])
            for section in selected_sections:
                status = rng.choices(REGISTRATION_STATUSES, weights=[88, 7, 5], k=1)[0]
                credits = 3.0 if status != "Dropped" else 0.0
                if status in {"Registered", "Withdrawn"}:
                    total_credits += credits
                    active_registration_count += 1
                registrations.append(
                    {
                        "registration_id": f"REG{len(registrations) + 1:06d}",
                        "student_id": student["student_id"],
                        "section_id": section["section_id"],
                        "term_id": term_id,
                        "registration_date": (term_start(term_id) - timedelta(days=rng.randint(1, 28))).isoformat(),
                        "registration_status": status,
                        "credit_hours": f"{credits:.1f}",
                        "grade_mode": rng.choice(["Letter", "Pass Fail", "Audit"]),
                    }
                )
            census_flag = active_registration_count > 0 and total_credits > 0
            enrollment.append(
                {
                    "enrollment_id": f"ENR{len(enrollment) + 1:06d}",
                    "student_id": student["student_id"],
                    "term_id": term_id,
                    "school_id": school_id,
                    "program_id": program_id,
                    "census_enrolled_flag": str(census_flag).lower(),
                    "ipeds_enrolled_flag": str(census_flag and total_credits >= 3.0).lower(),
                    "total_credit_hours": f"{total_credits:.1f}",
                    "enrollment_status": "Enrolled" if census_flag else "Not Enrolled",
                }
            )
    return registrations, enrollment


def term_start(term_id: str) -> date:
    for candidate, _, _, start, _, _ in TERMS:
        if candidate == term_id:
            return start
    raise ValueError(f"Unknown term_id: {term_id}")


def budget_rows(rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for fiscal_year in ["FY2025", "FY2026"]:
        for school_index, (school_id, _, _) in enumerate(SCHOOLS, start=1):
            base = 8_000_000 + school_index * 650_000
            revenue_budget = base + rng.randint(-250_000, 250_000)
            revenue_actual = revenue_budget + rng.randint(-350_000, 420_000)
            expense_budget = base * 0.82 + rng.randint(-175_000, 175_000)
            expense_actual = expense_budget + rng.randint(-275_000, 300_000)
            rows.append(
                {
                    "budget_actual_id": f"FIN{len(rows) + 1:04d}",
                    "fiscal_year": fiscal_year,
                    "school_id": school_id,
                    "revenue_budget": f"{revenue_budget:.2f}",
                    "revenue_actual": f"{revenue_actual:.2f}",
                    "expense_budget": f"{expense_budget:.2f}",
                    "expense_actual": f"{expense_actual:.2f}",
                }
            )
    return rows


def main() -> None:
    rng = random.Random(SEED)
    schools = school_rows()
    programs = program_rows()
    students = student_rows(rng, programs)
    terms = term_rows()
    sections = section_rows(rng, programs)
    applications, admissions, deposits = application_rows(rng, students, programs)
    registrations, enrollment = registration_and_enrollment_rows(rng, students, sections)
    budgets = budget_rows(rng)

    write_csv(OUTPUT_DIR / "schools.csv", ["school_id", "school_name", "school_code"], schools)
    write_csv(OUTPUT_DIR / "programs.csv", ["program_id", "school_id", "program_name", "degree_level", "cip_code"], programs)
    write_csv(
        OUTPUT_DIR / "students.csv",
        [
            "student_id",
            "student_type",
            "residency_status",
            "entry_term_id",
            "admit_school_id",
            "admit_program_id",
            "synthetic_birth_year",
        ],
        students,
    )
    write_csv(
        OUTPUT_DIR / "terms.csv",
        ["term_id", "term_name", "academic_year", "term_start_date", "census_date", "term_end_date"],
        terms,
    )
    write_csv(
        OUTPUT_DIR / "course_sections.csv",
        ["section_id", "term_id", "school_id", "program_id", "course_code", "section_number", "modality", "capacity"],
        sections,
    )
    write_csv(
        OUTPUT_DIR / "applications.csv",
        ["application_id", "student_id", "term_id", "school_id", "program_id", "application_date", "application_status"],
        applications,
    )
    write_csv(
        OUTPUT_DIR / "admissions.csv",
        ["admission_id", "application_id", "decision_date", "decision_status"],
        admissions,
    )
    write_csv(
        OUTPUT_DIR / "deposits.csv",
        ["deposit_id", "admission_id", "deposit_date", "deposit_status", "deposit_amount"],
        deposits,
    )
    write_csv(
        OUTPUT_DIR / "registrations.csv",
        ["registration_id", "student_id", "section_id", "term_id", "registration_date", "registration_status", "credit_hours", "grade_mode"],
        registrations,
    )
    write_csv(
        OUTPUT_DIR / "enrollment_census.csv",
        [
            "enrollment_id",
            "student_id",
            "term_id",
            "school_id",
            "program_id",
            "census_enrolled_flag",
            "ipeds_enrolled_flag",
            "total_credit_hours",
            "enrollment_status",
        ],
        enrollment,
    )
    write_csv(
        OUTPUT_DIR / "budget_actuals.csv",
        ["budget_actual_id", "fiscal_year", "school_id", "revenue_budget", "revenue_actual", "expense_budget", "expense_actual"],
        budgets,
    )

    print(f"Generated deterministic synthetic data in {OUTPUT_DIR}/ with seed {SEED}.")
    print(f"Schools: {len(schools)}")
    print(f"Programs: {len(programs)}")
    print(f"Students: {len(students)}")
    print(f"Terms: {len(terms)}")
    print(f"Sections: {len(sections)}")
    print(f"Applications: {len(applications)}")
    print(f"Admissions: {len(admissions)}")
    print(f"Deposits: {len(deposits)}")
    print(f"Registrations: {len(registrations)}")
    print(f"Enrollment rows: {len(enrollment)}")
    print(f"Budget rows: {len(budgets)}")


if __name__ == "__main__":
    main()
