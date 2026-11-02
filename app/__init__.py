"""FuturePath — personalised career and stream guidance for Class 10+ students.

Flask application factory and all HTTP routes.
"""
import json
import os
import random

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)

from . import db, engine, images

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )
    app.secret_key = os.environ.get("FUTUREPATH_SECRET", "futurepath-dev-secret")

    # Image helpers are available in every template as functions.
    app.jinja_env.globals.update(
        career_image=images.career_image,
        stream_image=images.stream_image,
        category_image=images.category_image,
        editorial_image=images.editorial_image,
        cover_for=images.cover_for,
        mentor_image=images.mentor_image,
    )

    db.init_db()
    register_routes(app)
    return app


def current_student():
    sid = session.get("student_id")
    if not sid:
        return None
    return db.query("SELECT * FROM students WHERE id = ?", (sid,), one=True)


def load_json(value, default):
    try:
        return json.loads(value) if value else default
    except (TypeError, ValueError):
        return default


def register_routes(app):
    # ------------------------------------------------------------------ pages
    @app.get("/")
    def index():
        student = current_student()
        dashboard = engine.profile_dashboard(student["id"]) if student else None
        # A different mentor portrait each visit; index is passed to the helper.
        mentor_seed = random.randrange(images.mentor_count())
        return render_template(
            "index.html",
            student=student,
            dashboard=dashboard,
            mentor_seed=mentor_seed,
            streams=db.query("SELECT * FROM streams ORDER BY sort_order"),
            careers=db.query("SELECT * FROM careers ORDER BY sort_order"),
        )

    @app.get("/assessment")
    def assessment_page():
        student = current_student()
        if not student:
            return redirect(url_for("index"))
        questions = db.query("SELECT * FROM assessment_questions ORDER BY kind, sort_order")
        grouped = {"interest": [], "skill": [], "preference": []}
        for q in questions:
            grouped.setdefault(q["kind"], []).append(dict(q))
        answers = {
            r["question_id"]: r["score"]
            for r in db.query(
                "SELECT question_id, score FROM assessment_answers WHERE student_id = ?",
                (student["id"],))
        }
        academics = {
            r["subject"]: r["marks"]
            for r in db.query(
                "SELECT subject, marks FROM academic_records WHERE student_id = ?",
                (student["id"],))
        }
        return render_template("assessment.html", student=student,
                               grouped=grouped, answers=answers, academics=academics)

    @app.get("/results")
    def results_page():
        student = current_student()
        if not student:
            return redirect(url_for("index"))
        result = engine.recommend_for_student(student["id"])
        return render_template("results.html", student=student, result=result)

    @app.get("/profile")
    def profile_page():
        student = current_student()
        if not student:
            return redirect(url_for("index"))
        data = engine.profile_dashboard(student["id"])
        data.pop("student", None)  # already passed explicitly below
        return render_template("profile.html", student=student, **data)

    @app.get("/careers")
    def careers_page():
        field = request.args.get("field")
        stream = request.args.get("stream")
        rows = db.query("SELECT * FROM careers ORDER BY sort_order")
        careers = []
        for r in rows:
            c = dict(r)
            for key in ("skills", "subjects_needed", "stream_slugs", "exams"):
                c[key] = load_json(c[key], [])
            c["riasec"] = load_json(c["riasec"], {})
            c["image"] = images.career_image(c["slug"])
            careers.append(c)
        if field:
            careers = [c for c in careers if c["field"] == field]
        stream_obj = None
        if stream:
            stream_obj = db.query("SELECT * FROM streams WHERE slug = ?", (stream,), one=True)
            careers = [c for c in careers if stream in c["stream_slugs"]]
        fields = sorted({c["field"] for c in careers} | {
            r["field"] for r in db.query("SELECT DISTINCT field FROM careers")})
        return render_template("careers.html", student=current_student(),
                               careers=careers, fields=fields, active=field,
                               stream_obj=dict(stream_obj) if stream_obj else None,
                               stream_slug=stream or "")

    @app.get("/career/<slug>")
    def career_detail(slug):
        row = db.query("SELECT * FROM careers WHERE slug = ?", (slug,), one=True)
        if not row:
            return "Career not found", 404
        career = dict(row)
        for key in ("skills", "subjects_needed", "stream_slugs", "exams"):
            career[key] = load_json(career[key], [])
        career["riasec"] = load_json(career["riasec"], {})

        streams = {
            s["slug"]: dict(s)
            for s in db.query("SELECT * FROM streams WHERE slug IN (%s)"
                              % ",".join("?" * len(career["stream_slugs"])),
                              tuple(career["stream_slugs"]))
        } if career["stream_slugs"] else {}

        exams = db.query("SELECT * FROM exams") if career["exams"] else []
        exam_map = {e["slug"]: dict(e) for e in exams}

        courses = []
        for c in db.query("SELECT * FROM courses"):
            if slug in load_json(c["careers"], []):
                d = dict(c)
                courses.append(d)

        return render_template("career.html", student=current_student(), career=career,
                               streams=streams, exam_map=exam_map, courses=courses,
                               cover=images.cover_for(slug),
                               hero_image=images.career_image(slug, 1200, 760),
                               category_image=images.category_image(career["field"]))

    @app.get("/compare")
    def compare_page():
        slugs = request.args.get("c") or request.args.getlist("career")
        if isinstance(slugs, str):
            slugs = [s for s in slugs.split(",") if s]
        careers = []
        for slug in slugs[:3]:
            row = db.query("SELECT * FROM careers WHERE slug = ?", (slug,), one=True)
            if not row:
                continue
            c = dict(row)
            for key in ("skills", "subjects_needed", "stream_slugs", "exams"):
                c[key] = load_json(c[key], [])
            c["riasec"] = load_json(c["riasec"], {})
            careers.append(c)
        all_careers = db.query("SELECT slug, name, icon FROM careers ORDER BY sort_order")
        return render_template("compare.html", student=current_student(),
                               careers=careers, all_careers=all_careers)

    @app.get("/exams")
    def exams_page():
        rows = db.query("SELECT * FROM exams ORDER BY name")
        exams = []
        for r in rows:
            e = dict(r)
            e["for_streams"] = load_json(e["for_streams"], [])
            e["syllabus"] = load_json(e["syllabus"], [])
            exams.append(e)
        return render_template("exams.html", student=current_student(), exams=exams,
                               scholarships=db.query("SELECT * FROM scholarships ORDER BY name"))

    @app.get("/roadmap")
    def roadmap_page():
        student = current_student()
        if not student:
            return redirect(url_for("index"))
        slug = request.args.get("career")
        if not slug:
            top = engine.recommend_for_student(student["id"])["top_career"]
            slug = top["slug"] if top else None
        if not slug:
            return redirect(url_for("results_page"))
        roadmap = engine.build_roadmap(student["id"], slug)
        if not roadmap:
            return "Career not found", 404
        return render_template("roadmap.html", student=student, roadmap=roadmap)

    # ------------------------------------------------------------------- auth
    @app.post("/api/register")
    def api_register():
        data = request.get_json(force=True, silent=True) or {}
        username = (data.get("username") or "").strip().lower()
        password = data.get("password") or ""
        if len(username) < 3 or len(password) < 4:
            return jsonify({"error": "username 3+ characters, password 4+ characters"}), 400
        if db.query("SELECT id FROM students WHERE username = ?", (username,), one=True):
            return jsonify({"error": "that username is taken"}), 409
        sid = db.execute(
            """INSERT INTO students (username, display_name, password_hash, class_level,
                                     board, state, city, medium)
               VALUES (?,?,?,?,?,?,?,?)""",
            (username, (data.get("display_name") or username).strip(),
             engine.hash_password(password),
             data.get("class_level", "Class 10"), data.get("board", "CBSE"),
             data.get("state", ""), data.get("city", ""), data.get("medium", "English")),
        )
        session["student_id"] = sid
        return jsonify({"ok": True, "student_id": sid})

    @app.post("/api/login")
    def api_login():
        data = request.get_json(force=True, silent=True) or {}
        student = db.query("SELECT * FROM students WHERE username = ?",
                           ((data.get("username") or "").strip().lower(),), one=True)
        if not student or not engine.check_password(data.get("password") or "",
                                                    student["password_hash"]):
            return jsonify({"error": "invalid username or password"}), 401
        session["student_id"] = student["id"]
        return jsonify({"ok": True, "student_id": student["id"]})

    @app.post("/api/logout")
    def api_logout():
        session.pop("student_id", None)
        return jsonify({"ok": True})

    # --------------------------------------------------------------- profile API
    @app.post("/api/academics")
    def api_academics():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        data = request.get_json(force=True, silent=True) or {}
        subjects = data.get("subjects") or {}
        db.execute("DELETE FROM academic_records WHERE student_id = ?", (student["id"],))
        for subject, marks in subjects.items():
            try:
                value = float(marks)
            except (TypeError, ValueError):
                continue
            db.execute(
                "INSERT INTO academic_records (student_id, subject, marks) VALUES (?,?,?)",
                (student["id"], subject, value),
            )
        return jsonify({"ok": True, "saved": len(subjects)})

    @app.post("/api/assessment/answer")
    def api_assessment_answer():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        data = request.get_json(force=True, silent=True) or {}
        qid, score = int(data.get("question_id")), int(data.get("score"))
        existing = db.query(
            "SELECT id FROM assessment_answers WHERE student_id = ? AND question_id = ?",
            (student["id"], qid), one=True)
        if existing:
            db.execute("UPDATE assessment_answers SET score = ? WHERE id = ?",
                       (score, existing["id"]))
        else:
            db.execute(
                "INSERT INTO assessment_answers (student_id, question_id, score) VALUES (?,?,?)",
                (student["id"], qid, score))
        return jsonify({"ok": True})

    @app.post("/api/profile/update")
    def api_profile_update():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        data = request.get_json(force=True, silent=True) or {}
        fields = {
            "display_name": (data.get("display_name") or "").strip(),
            "class_level": data.get("class_level") or student["class_level"],
            "board": data.get("board") or student["board"],
            "state": (data.get("state") or "").strip(),
            "city": (data.get("city") or "").strip(),
            "medium": data.get("medium") or student["medium"],
        }
        if not fields["display_name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        db.execute(
            """UPDATE students SET display_name = ?, class_level = ?, board = ?,
                   state = ?, city = ?, medium = ? WHERE id = ?""",
            (fields["display_name"], fields["class_level"], fields["board"],
             fields["state"], fields["city"], fields["medium"], student["id"]))
        return jsonify({"ok": True})

    @app.post("/api/profile/password")
    def api_profile_password():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        data = request.get_json(force=True, silent=True) or {}
        current = data.get("current") or ""
        new = data.get("new") or ""
        if not engine.check_password(current, student["password_hash"]):
            return jsonify({"error": "current password is not correct"}), 400
        if len(new) < 6:
            return jsonify({"error": "new password must be at least 6 characters"}), 400
        db.execute("UPDATE students SET password_hash = ? WHERE id = ?",
                   (engine.hash_password(new), student["id"]))
        return jsonify({"ok": True})

    @app.post("/api/profile/reset-assessment")
    def api_profile_reset():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        db.execute("DELETE FROM assessment_answers WHERE student_id = ?", (student["id"],))
        return jsonify({"ok": True})

    @app.post("/api/profile/reset-academics")
    def api_profile_reset_academics():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        db.execute("DELETE FROM academic_records WHERE student_id = ?", (student["id"],))
        return jsonify({"ok": True})

    @app.get("/api/profile/summary")
    def api_profile_summary():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        return jsonify(engine.profile_dashboard(student["id"]))

    @app.get("/api/profile")
    def api_profile():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        return jsonify(engine.profile_for_student(student["id"]))

    @app.post("/api/roadmap/toggle")
    def api_roadmap_toggle():
        student = current_student()
        if not student:
            return jsonify({"error": "not signed in"}), 401
        data = request.get_json(force=True, silent=True) or {}
        row = db.query(
            "SELECT id, checklist FROM roadmaps WHERE student_id = ? AND career_slug = ?",
            (student["id"], data.get("career")), one=True)
        if not row:
            return jsonify({"error": "no roadmap for that career yet"}), 404
        checklist = load_json(row["checklist"], {})
        key = str(int(data.get("index")))
        checklist[key] = not checklist.get(key, False)
        db.execute("UPDATE roadmaps SET checklist = ? WHERE id = ?",
                   (json.dumps(checklist), row["id"]))
        done = sum(1 for v in checklist.values() if v)
        return jsonify({"ok": True, "done": done, "total": len(checklist)})

    @app.get("/healthz")
    def healthz():
        return jsonify({"ok": True})
