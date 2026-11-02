"""Recommendation engine and roadmap builder.

How the match works
-------------------
Each career and stream declares a desired profile:
  * `riasec`  — weights over Holland's six dimensions, 0..1
  * `skills`  — the skills that matter for the work
  * `subjects_needed` — school subjects that feed into it

A student's profile is built from three signals:
  1. academic performance (subject-wise marks, normalised)
  2. interest (RIASEC inventory, normalised to 0..1 per dimension)
  3. skill self-ratings (normalised)

The match score is a weighted cosine-style similarity between the two vectors,
plus an academic-fit term. Weights are declared in WEIGHTS so the balance can be
tuned (or learned) without touching the algorithm.
"""
import hashlib
import hmac
import json
import os

from . import db

# How much each signal contributes to the final match score.
WEIGHTS = {
    "interest": 0.45,   # RIASEC alignment — the strongest signal
    "skills": 0.30,     # self-rated ability
    "academic": 0.25,   # subject marks that the career actually depends on
}

RIASEC_DIMENSIONS = ["R", "I", "A", "S", "E", "C"]

RIASEC_LABELS = {
    "R": "Realistic — hands-on, building, machines, tools",
    "I": "Investigative — analysis, research, problem-solving",
    "A": "Artistic — creativity, design, expression",
    "S": "Social — helping, teaching, caring for people",
    "E": "Enterprising — leading, persuading, business",
    "C": "Conventional — organising, systems, accuracy",
}

# Which school subjects feed which career families. Used for the academic term.
SUBJECT_ALIASES = {
    "mathematics": "maths", "maths": "maths", "math": "maths",
    "physics": "physics", "chemistry": "chemistry", "biology": "biology",
    "science": "science", "computer science": "computers", "computers": "computers",
    "english": "english", "social science": "social", "history": "history",
    "geography": "geography", "economics": "economics", "accountancy": "accounts",
    "business studies": "business", "commerce": "commerce",
    "political science": "political", "psychology": "psychology",
    "fine arts": "art", "art": "art", "physical education": "pe",
}


# ------------------------------------------------------------------- passwords
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"pbkdf2_sha256$120000${salt.hex()}${digest.hex()}"


def check_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt_hex, digest_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(),
                                     bytes.fromhex(salt_hex), int(iterations))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False


# ------------------------------------------------------------------- profiles
def _normalise_subject(name):
    key = (name or "").strip().lower()
    return SUBJECT_ALIASES.get(key, key)


def profile_for_student(student_id):
    """Build the student's profile vector from the three signals."""
    records = db.query(
        "SELECT subject, marks FROM academic_records WHERE student_id = ?", (student_id,))
    academics = {}
    for r in records:
        academics[_normalise_subject(r["subject"])] = float(r["marks"])

    answers = db.query(
        """SELECT aq.kind, aq.dimension, AVG(aa.score) AS avg_score
           FROM assessment_answers aa
           JOIN assessment_questions aq ON aq.id = aa.question_id
           WHERE aa.student_id = ?
           GROUP BY aq.kind, aq.dimension""",
        (student_id,),
    )

    interest = {d: 0.0 for d in RIASEC_DIMENSIONS}
    skills = {}
    counts = {"interest": 0, "skill": 0}
    for a in answers:
        if a["kind"] == "interest":
            # Likert 1..5 -> 0..1
            interest[a["dimension"]] = round((a["avg_score"] - 1) / 4, 3)
            counts["interest"] += 1
        elif a["kind"] == "skill":
            skills[a["dimension"]] = round((a["avg_score"] - 1) / 4, 3)
            counts["skill"] += 1

    completed = bool(counts["interest"])
    return {
        "interest": interest,
        "skills": skills,
        "academics": academics,
        "interest_answered": counts["interest"],
        "skills_answered": counts["skill"],
        "academics_entered": len(academics),
        "completed": completed,
    }


# --------------------------------------------------------------------- scoring
def _cosine(a, b):
    """Weighted similarity of two {dimension: weight} maps, 0..1."""
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _academic_fit(career_subjects, academics):
    """How well the student's marks support the subjects this career needs."""
    if not career_subjects:
        return 0.5  # neutral when the career does not depend on specific subjects
    wanted = [_normalise_subject(s) for s in career_subjects]
    scores = [academics[w] / 100.0 for w in wanted if w in academics]
    if not scores:
        return 0.4  # no data: neither a boost nor a penalty
    return sum(scores) / len(scores)


def score_career(profile, career):
    interest = _cosine(profile["interest"], career["riasec"])
    skill_map = {s: 0.8 for s in career["skills"]}  # desired skills are weighted equally
    skills = _cosine(profile["skills"], skill_map) if profile["skills"] else 0.0
    academic = _academic_fit(career["subjects_needed"], profile["academics"])

    total = (WEIGHTS["interest"] * interest
             + WEIGHTS["skills"] * skills
             + WEIGHTS["academic"] * academic)

    # With no assessment data yet, fall back to academics alone so the page is
    # still useful rather than showing everything at zero.
    if not profile["skills"]:
        total = (WEIGHTS["interest"] + WEIGHTS["skills"] * 0.5) * interest \
            + WEIGHTS["academic"] * academic
    return {
        "score": round(total * 100, 1),
        "parts": {
            "interest": round(interest * 100, 1),
            "skills": round(skills * 100, 1),
            "academic": round(academic * 100, 1),
        },
    }


def _load_careers():
    careers = []
    for row in db.query("SELECT * FROM careers ORDER BY sort_order"):
        c = dict(row)
        c["riasec"] = json.loads(c["riasec"] or "{}")
        for key in ("skills", "subjects_needed", "stream_slugs", "exams"):
            c[key] = json.loads(c[key] or "[]")
        careers.append(c)
    return careers


def _load_streams():
    streams = []
    for row in db.query("SELECT * FROM streams ORDER BY sort_order"):
        s = dict(row)
        s["riasec"] = json.loads(s["riasec"] or "{}")
        for key in ("subjects", "paths_after"):
            s[key] = json.loads(s[key] or "[]")
        streams.append(s)
    return streams


def recommend_for_student(student_id, top_n=6):
    """Rank every career for this student and aggregate the stream signals."""
    profile = profile_for_student(student_id)
    careers = _load_careers()

    scored = []
    for c in careers:
        result = score_career(profile, c)
        scored.append({**c, "match": result["score"], "parts": result["parts"]})
    scored.sort(key=lambda c: c["match"], reverse=True)

    # A stream's score is the best career it leads to, plus a small bonus for
    # each additional strong career — a stream that opens several doors is better
    # than one that leads to a single job.
    stream_scores = {}
    for c in scored:
        for slug in c["stream_slugs"]:
            entry = stream_scores.setdefault(slug, {"best": 0.0, "count": 0, "careers": []})
            entry["best"] = max(entry["best"], c["match"])
            if c["match"] >= 60:
                entry["count"] += 1
            entry["careers"].append({"name": c["name"], "match": c["match"]})

    streams = []
    for s in _load_streams():
        entry = stream_scores.get(s["slug"])
        if not entry:
            continue
        breadth_bonus = min(entry["count"], 5) * 1.2
        s = {**s, "match": round(min(100.0, entry["best"] + breadth_bonus), 1),
             "career_count": entry["count"],
             "top_careers": sorted(entry["careers"], key=lambda x: -x["match"])[:4]}
        streams.append(s)
    streams.sort(key=lambda s: s["match"], reverse=True)

    return {
        "profile": profile,
        "riasec_labels": RIASEC_LABELS,
        "careers": scored,
        "top_career": scored[0] if scored else None,
        "streams": streams,
        "top_stream": streams[0] if streams else None,
        "weights": WEIGHTS,
    }


# The six stages the roadmap visualiser draws. Each generated plan step is
# mapped onto one of these, so the diagram always reflects the student's real
# roadmap rather than being decorative.
ROADMAP_STAGES = [
    ("goal",     "Career goal",  "🎯"),
    ("study",    "Subjects",     "📚"),
    ("exam",     "Entrance exams", "📝"),
    ("apply",    "Courses & colleges", "🏛️"),
    ("fund",     "Scholarships", "🎓"),
    ("growth",   "Skills & internships", "🚀"),
]

STAGE_FOR_KIND = {
    "decision": "goal",
    "study": "study",
    "exam": "exam",
    "application": "apply",
    "scholarship": "fund",
    "growth": "growth",
}


def roadmap_stages(plan):
    """Collapse a roadmap plan into the six visual stages, with progress."""
    by_stage = {key: {"key": key, "label": label, "icon": icon,
                      "steps": [], "done": 0} for key, label, icon in ROADMAP_STAGES}
    for i, step in enumerate(plan):
        key = STAGE_FOR_KIND.get(step.get("kind"), "goal")
        by_stage[key]["steps"].append(i)
    return [by_stage[k] for k, _, _ in ROADMAP_STAGES]


# ---------------------------------------------------------------- dashboard
def profile_dashboard(student_id):
    """Everything the profile page needs, in one call.

    Gives the student a sense of progress: how complete their profile is, what
    they have done, and what the next action is.
    """
    student = db.query("SELECT * FROM students WHERE id = ?", (student_id,), one=True)
    profile = profile_for_student(student_id)

    # Preferences are not scored, but they are still part of the questionnaire,
    # so completion counts all three kinds.
    counts = {
        r["kind"]: r["n"]
        for r in db.query(
            "SELECT kind, COUNT(*) AS n FROM assessment_questions GROUP BY kind")
    }
    total_questions = sum(counts.values())
    preference_answered = db.query(
        """SELECT COUNT(*) AS n FROM assessment_answers aa
           JOIN assessment_questions aq ON aq.id = aa.question_id
           WHERE aa.student_id = ? AND aq.kind = 'preference'""",
        (student_id,), one=True)["n"]
    answered = (profile["interest_answered"] + profile["skills_answered"]
                + preference_answered)
    profile["preference_answered"] = preference_answered
    completion = round(100 * answered / total_questions) if total_questions else 0

    academics = db.query(
        """SELECT subject, marks FROM academic_records
           WHERE student_id = ? ORDER BY marks DESC""", (student_id,))
    average = round(sum(a["marks"] for a in academics) / len(academics), 1) if academics else 0

    roadmaps = db.query(
        "SELECT * FROM roadmaps WHERE student_id = ? ORDER BY created_at DESC",
        (student_id,))
    roadmap_rows = []
    for r in roadmaps:
        plan = json.loads(r["plan"] or "[]")
        checklist = json.loads(r["checklist"] or "{}")
        career = db.query("SELECT name, icon FROM careers WHERE slug = ?",
                          (r["career_slug"],), one=True)
        roadmap_rows.append({
            "career_slug": r["career_slug"],
            "career_name": career["name"] if career else r["career_slug"],
            "icon": career["icon"] if career else "🗺️",
            "done": sum(1 for v in checklist.values() if v),
            "total": len(plan),
            "created_at": r["created_at"],
        })

    result = recommend_for_student(student_id)

    # A single, obvious next action, so the page is never a dead end.
    if answered < total_questions:
        next_action = {
            "label": "Finish your assessment",
            "detail": f"{total_questions - answered} question(s) left — it takes about "
                      f"{max(1, (total_questions - answered) // 4)} minute(s).",
            "url": "/assessment",
            "cta": "Continue assessment",
        }
    elif not academics:
        next_action = {
            "label": "Add your subject marks",
            "detail": "Your marks carry 25% of every match score.",
            "url": "/assessment",
            "cta": "Enter marks",
        }
    elif not roadmap_rows:
        next_action = {
            "label": "Build your roadmap",
            "detail": "Turn your top match into a step-by-step plan with exams and deadlines.",
            "url": f"/roadmap?career={result['top_career']['slug']}" if result["top_career"] else "/results",
            "cta": "Open roadmap",
        }
    else:
        next_action = {
            "label": "Compare your top options",
            "detail": "Put two or three careers side by side before you decide.",
            "url": "/compare",
            "cta": "Compare careers",
        }

    stages = []
    if roadmap_rows:
        newest = db.query(
            "SELECT * FROM roadmaps WHERE student_id = ? ORDER BY created_at DESC LIMIT 1",
            (student_id,), one=True)
        newest_plan = json.loads(newest["plan"] or "[]")
        newest_checklist = json.loads(newest["checklist"] or "{}")
        stages = roadmap_stages(newest_plan)
        for st in stages:
            st["done"] = sum(1 for i in st["steps"] if newest_checklist.get(str(i)))
            st["total"] = len(st["steps"])

    return {
        "profile": profile,
        "student": dict(student) if student else {},
        "completion": completion,
        "stages": stages,
        "answered": answered,
        "total_questions": total_questions,
        "academics": [dict(a) for a in academics],
        "average_marks": average,
        "roadmaps": roadmap_rows,
        "result": result,
        "next_action": next_action,
        "riasec_labels": RIASEC_LABELS,
    }


# ------------------------------------------------------------------- roadmaps
def build_roadmap(student_id, career_slug):
    """Generate the step-by-step plan"""
    row = db.query("SELECT * FROM careers WHERE slug = ?", (career_slug,), one=True)
    if not row:
        return None
    career = dict(row)
    career["subjects_needed"] = json.loads(career["subjects_needed"] or "[]")
    career["stream_slugs"] = json.loads(career["stream_slugs"] or "[]")
    career["exams"] = json.loads(career["exams"] or "[]")

    stream = None
    if career["stream_slugs"]:
        stream = db.query("SELECT * FROM streams WHERE slug = ?",
                          (career["stream_slugs"][0],), one=True)
        stream = dict(stream) if stream else None
        if stream:
            stream["subjects"] = json.loads(stream["subjects"] or "[]")

    exams = []
    for slug in career["exams"]:
        e = db.query("SELECT * FROM exams WHERE slug = ?", (slug,), one=True)
        if e:
            d = dict(e)
            d["syllabus"] = json.loads(d["syllabus"] or "[]")
            exams.append(d)

    student = db.query("SELECT * FROM students WHERE id = ?", (student_id,), one=True)
    class_level = student["class_level"] if student else "Class 10"

    # Scholarships the student plausibly qualifies for: by stream, and any that
    # are open to all.
    scholarships = []
    for s in db.query("SELECT * FROM scholarships"):
        d = dict(s)
        d["for_streams"] = json.loads(d["for_streams"] or "[]")
        if not d["for_streams"] or (stream and stream["slug"] in d["for_streams"]):
            scholarships.append(d)

    plan = []

    # 1. Stream choice
    plan.append({
        "phase": f"Now — {class_level}",
        "title": f"Choose the {stream['name']} stream" if stream else "Confirm your stream",
        "detail": (stream["summary"] if stream else
                   "This career is open from more than one stream; talk to your school counsellor "
                   "about which route fits your subjects."),
        "actions": ([f"Pick these subjects: {', '.join(stream['subjects'])}"]
                    if stream else []) + [
            "Speak to two people already working in this field",
            "Check the subject combination against your board's rules",
        ],
        "kind": "decision",
    })

    # 2. Class 11-12 focus
    plan.append({
        "phase": "Class 11–12",
        "title": "Build the foundation subjects",
        "detail": "These are the school subjects this career actually leans on. "
                  "Aim for consistency rather than last-minute cramming.",
        "actions": [f"Prioritise {s}" for s in career["subjects_needed"]] or
                   ["Keep all core subjects strong"],
        "kind": "study",
    })

    # 3. Entrance exams
    if exams:
        for e in exams:
            months = e["prep_months"] or 12
            plan.append({
                "phase": f"{months} months before {e['name']}",
                "title": f"Prepare for {e['name']}",
                "detail": f"{e['full_name'] or e['name']} — {e['eligibility']}. "
                          f"Held around {e['when_held']}.",
                "actions": [f"Cover: {s}" for s in e["syllabus"]] or
                           ["Follow the official syllabus"],
                "kind": "exam",
            })
    else:
        plan.append({
            "phase": "Class 12",
            "title": "Focus on board results",
            "detail": "This career route does not require a national entrance exam, "
                      "so your board percentage and portfolio carry the weight.",
            "actions": ["Build a portfolio of relevant work", "Shortlist colleges and courses"],
            "kind": "study",
        })

    # 4. Applications
    plan.append({
        "phase": "Application window",
        "title": "Apply to colleges and courses",
        "detail": "Apply to a spread: two ambitious choices, three realistic ones, "
                  "and one safe option.",
        "actions": ["Track every deadline in one calendar",
                    "Keep documents and certificates ready"],
        "kind": "application",
    })

    # 5. Scholarships
    if scholarships:
        plan.append({
            "phase": "Alongside applications",
            "title": f"Apply for {len(scholarships)} scholarship(s) you may qualify for",
            "detail": "Most students skip these. Deadlines usually fall earlier than "
                      "admission deadlines, so apply early.",
            "actions": [f"{s['name']} — {s['amount']} ({s['provider']})" for s in scholarships],
            "kind": "scholarship",
        })

    # 6. Long term
    plan.append({
        "phase": "During your degree",
        "title": "Build proof of work, not just marks",
        "detail": "Internships, projects and certifications are what separate two "
                  "candidates with the same degree.",
        "actions": ["Do at least two internships before final year",
                    "Build a portfolio you can show",
                    "Find a mentor in the field"],
        "kind": "growth",
    })

    existing = db.query(
        "SELECT * FROM roadmaps WHERE student_id = ? AND career_slug = ?",
        (student_id, career_slug), one=True)
    if existing:
        db.execute("UPDATE roadmaps SET plan = ?, created_at = datetime('now') WHERE id = ?",
                   (json.dumps(plan), existing["id"]))
        checklist = json.loads(existing["checklist"] or "{}")
    else:
        db.execute(
            "INSERT INTO roadmaps (student_id, career_slug, plan, checklist) VALUES (?,?,?,?)",
            (student_id, career_slug, json.dumps(plan), "{}"))
        checklist = {}

    return {
        "career": career,
        "stream": stream,
        "exams": exams,
        "scholarships": scholarships,
        "plan": plan,
        "checklist": checklist,
        "done": sum(1 for v in checklist.values() if v),
        "total": len(plan),
    }
