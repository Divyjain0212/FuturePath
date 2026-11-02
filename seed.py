"""Create the database and load the knowledge base.

    python seed.py            (safe to re-run: content is upserted by slug)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import db  # noqa: E402
from app import knowledge as K  # noqa: E402


def seed_assessment():
    """Upsert assessment questions.

    Deliberately NOT a delete-and-recreate: assessment_answers has a foreign key
    onto these rows, so recreating them would cascade-delete every student's
    answers. Existing questions are matched on (kind, prompt) and updated in
    place, so reseeding the knowledge base never destroys student data.
    """
    rows = []
    order = 0
    for dimension, prompt in K.INTEREST_QUESTIONS:
        rows.append(("interest", dimension, prompt, order)); order += 1
    order = 0
    for dimension, prompt in K.SKILL_QUESTIONS:
        rows.append(("skill", dimension, prompt, order)); order += 1
    order = 0
    for dimension, prompt in K.PREFERENCE_QUESTIONS:
        rows.append(("preference", dimension, prompt, order)); order += 1

    for kind, dimension, prompt, sort_order in rows:
        existing = db.query(
            "SELECT id FROM assessment_questions WHERE kind = ? AND prompt = ?",
            (kind, prompt), one=True)
        if existing:
            db.execute(
                "UPDATE assessment_questions SET dimension = ?, sort_order = ? WHERE id = ?",
                (dimension, sort_order, existing["id"]))
        else:
            db.execute(
                """INSERT INTO assessment_questions (kind, dimension, prompt, sort_order)
                   VALUES (?,?,?,?)""",
                (kind, dimension, prompt, sort_order))
    return len(rows)


def upsert(table, slug, fields):
    """Insert or update a row identified by its slug."""
    existing = db.query(f"SELECT id FROM {table} WHERE slug = ?", (slug,), one=True)
    columns = ", ".join(fields.keys())
    placeholders = ", ".join("?" * len(fields))
    values = list(fields.values())
    if existing:
        assignments = ", ".join(f"{k} = ?" for k in fields)
        db.execute(f"UPDATE {table} SET {assignments} WHERE slug = ?", values + [slug])
    else:
        db.execute(f"INSERT INTO {table} (slug, {columns}) VALUES (?, {placeholders})",
                   [slug] + values)


def seed_streams():
    for s in K.STREAMS:
        upsert("streams", s["slug"], {
            "name": s["name"], "icon": s["icon"], "summary": s["summary"],
            "subjects": json.dumps(s["subjects"]),
            "who_it_suits": s["who_it_suits"],
            "paths_after": json.dumps(s["paths_after"]),
            "riasec": json.dumps(s["riasec"]),
            "sort_order": s["sort_order"],
        })
    return len(K.STREAMS)


def seed_careers():
    for c in K.CAREERS:
        upsert("careers", c["slug"], {
            "name": c["name"], "icon": c["icon"], "field": c["field"],
            "summary": c["summary"], "day_in_life": c["day_in_life"],
            "skills": json.dumps(c["skills"]),
            "subjects_needed": json.dumps(c["subjects_needed"]),
            "stream_slugs": json.dumps(c["stream_slugs"]),
            "riasec": json.dumps(c["riasec"]),
            "salary_start": c["salary_start"], "salary_mid": c["salary_mid"],
            "growth": c["growth"], "difficulty": c["difficulty"],
            "exams": json.dumps(c["exams"]), "sort_order": c["sort_order"],
        })
    return len(K.CAREERS)


def seed_exams():
    for e in K.EXAMS:
        upsert("exams", e["slug"], {
            "name": e["name"], "full_name": e["full_name"],
            "for_streams": json.dumps(e["for_streams"]),
            "eligibility": e["eligibility"], "when_held": e["when_held"],
            "window": e["window"], "syllabus": json.dumps(e["syllabus"]),
            "prep_months": e["prep_months"], "website": e["website"],
        })
    return len(K.EXAMS)


def seed_scholarships():
    for s in K.SCHOLARSHIPS:
        upsert("scholarships", s["slug"], {
            "name": s["name"], "provider": s["provider"], "amount": s["amount"],
            "eligibility": s["eligibility"],
            "for_streams": json.dumps(s["for_streams"]),
            "deadline": s["deadline"], "notes": s["notes"],
        })
    return len(K.SCHOLARSHIPS)


def seed_courses():
    for c in K.COURSES:
        upsert("courses", c["slug"], {
            "name": c["name"], "level": c["level"], "duration": c["duration"],
            "stream_slug": c["stream_slug"], "summary": c["summary"],
            "careers": json.dumps(c["careers"]),
        })
    return len(K.COURSES)


def seed_colleges():
    for c in K.COLLEGES:
        upsert("colleges", c["slug"], {
            "name": c["name"], "city": c["city"], "state": c["state"], "type": c["type"],
            "courses": json.dumps(c["courses"]),
            "entrance_exams": json.dumps(c["entrance_exams"]),
            "notes": c["notes"], "website": c["website"],
        })
    return len(K.COLLEGES)


def main():
    db.init_db()
    counts = {
        "assessment questions": seed_assessment(),
        "streams": seed_streams(),
        "careers": seed_careers(),
        "courses": seed_courses(),
        "colleges": seed_colleges(),
        "entrance exams": seed_exams(),
        "scholarships": seed_scholarships(),
    }
    print("FuturePath knowledge base loaded:")
    for label, n in counts.items():
        print(f"  {label:<22} {n}")


if __name__ == "__main__":
    main()
