"""Database layer for FuturePath.

SQLite keeps the project runnable anywhere with no setup. The schema student profile + academic record + assessment, a
knowledge base (streams, careers, courses, colleges, exams, scholarships), and
the generated outputs (recommendations, roadmaps).
"""
import os
import sqlite3

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "data", "futurepath.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------ students
CREATE TABLE IF NOT EXISTS students (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    display_name  TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    class_level   TEXT NOT NULL DEFAULT 'Class 10',   -- Class 10 | Class 11 | Class 12
    board         TEXT NOT NULL DEFAULT 'CBSE',       -- CBSE | ICSE | State Board | Other
    state         TEXT NOT NULL DEFAULT '',
    city          TEXT NOT NULL DEFAULT '',
    medium        TEXT NOT NULL DEFAULT 'English',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Subject-wise marks, the academic half of the profile.
CREATE TABLE IF NOT EXISTS academic_records (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject      TEXT NOT NULL,
    marks        REAL NOT NULL,          -- percentage in that subject
    exam_label   TEXT NOT NULL DEFAULT 'Class 10 Board',
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ----------------------------------------------------------------- assessment
-- RIASEC inventory and skill self-ratings, both stored as question banks so the
-- questionnaire can grow without code changes.
CREATE TABLE IF NOT EXISTS assessment_questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kind        TEXT NOT NULL,            -- interest | skill | preference
    dimension   TEXT NOT NULL,            -- R I A S E C, or logical/creative/...
    prompt      TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS assessment_answers (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    question_id  INTEGER NOT NULL REFERENCES assessment_questions(id) ON DELETE CASCADE,
    score        INTEGER NOT NULL,        -- 1..5 Likert, or 0..4 skill rating
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (student_id, question_id)
);

-- --------------------------------------------------------------- knowledge base
CREATE TABLE IF NOT EXISTS streams (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    icon          TEXT NOT NULL DEFAULT '',
    summary       TEXT NOT NULL DEFAULT '',
    subjects      TEXT NOT NULL DEFAULT '[]',   -- JSON list
    who_it_suits  TEXT NOT NULL DEFAULT '',
    paths_after   TEXT NOT NULL DEFAULT '[]',   -- JSON list of degree/career routes
    riasec        TEXT NOT NULL DEFAULT '{}',   -- JSON: ideal RIASEC profile weights
    sort_order    INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE IF NOT EXISTS careers (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    slug           TEXT NOT NULL UNIQUE,
    name           TEXT NOT NULL,
    icon           TEXT NOT NULL DEFAULT '',
    field          TEXT NOT NULL DEFAULT '',     -- Technology | Healthcare | Design ...
    summary        TEXT NOT NULL DEFAULT '',
    day_in_life    TEXT NOT NULL DEFAULT '',
    skills         TEXT NOT NULL DEFAULT '[]',
    subjects_needed TEXT NOT NULL DEFAULT '[]',
    stream_slugs   TEXT NOT NULL DEFAULT '[]',
    riasec         TEXT NOT NULL DEFAULT '{}',
    salary_start   TEXT NOT NULL DEFAULT '',
    salary_mid     TEXT NOT NULL DEFAULT '',
    growth         TEXT NOT NULL DEFAULT '',     -- outlook text
    difficulty     TEXT NOT NULL DEFAULT 'Moderate',
    exams          TEXT NOT NULL DEFAULT '[]',   -- JSON list of exam slugs
    sort_order     INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE IF NOT EXISTS courses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    slug         TEXT NOT NULL UNIQUE,
    name         TEXT NOT NULL,
    level        TEXT NOT NULL DEFAULT '',       -- Undergraduate | Diploma | Certificate
    duration     TEXT NOT NULL DEFAULT '',
    stream_slug  TEXT NOT NULL DEFAULT '',
    summary      TEXT NOT NULL DEFAULT '',
    careers      TEXT NOT NULL DEFAULT '[]'      -- JSON list of career slugs
);

CREATE TABLE IF NOT EXISTS colleges (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    slug         TEXT NOT NULL UNIQUE,
    name         TEXT NOT NULL,
    city         TEXT NOT NULL DEFAULT '',
    state        TEXT NOT NULL DEFAULT '',
    type         TEXT NOT NULL DEFAULT '',       -- Government | Private | Deemed
    courses      TEXT NOT NULL DEFAULT '[]',
    entrance_exams TEXT NOT NULL DEFAULT '[]',
    notes        TEXT NOT NULL DEFAULT '',
    website      TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS exams (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    slug         TEXT NOT NULL UNIQUE,
    name         TEXT NOT NULL,
    full_name    TEXT NOT NULL DEFAULT '',
    for_streams  TEXT NOT NULL DEFAULT '[]',
    eligibility  TEXT NOT NULL DEFAULT '',
    when_held    TEXT NOT NULL DEFAULT '',
    window       TEXT NOT NULL DEFAULT '',
    syllabus     TEXT NOT NULL DEFAULT '[]',
    prep_months  INTEGER NOT NULL DEFAULT 12,
    website      TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS scholarships (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    provider      TEXT NOT NULL DEFAULT '',
    amount        TEXT NOT NULL DEFAULT '',
    eligibility   TEXT NOT NULL DEFAULT '',
    for_streams   TEXT NOT NULL DEFAULT '[]',
    deadline      TEXT NOT NULL DEFAULT '',
    notes         TEXT NOT NULL DEFAULT ''
);

-- -------------------------------------------------------------------- outputs
-- A saved recommendation run: the profile snapshot plus the ranked result.
CREATE TABLE IF NOT EXISTS recommendations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    profile      TEXT NOT NULL DEFAULT '{}',   -- JSON: riasec + skills + academic
    results      TEXT NOT NULL DEFAULT '[]'    -- JSON: ranked streams and careers
);

CREATE TABLE IF NOT EXISTS roadmaps (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    career_slug  TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    plan         TEXT NOT NULL DEFAULT '[]',   -- JSON: ordered milestones
    checklist    TEXT NOT NULL DEFAULT '{}'    -- JSON: {milestone_index: done}
);

CREATE TABLE IF NOT EXISTS saved_comparisons (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    career_slugs TEXT NOT NULL DEFAULT '[]',
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = connect()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()


def query(sql, args=(), one=False):
    conn = connect()
    try:
        rows = conn.execute(sql, args).fetchall()
        return (rows[0] if rows else None) if one else rows
    finally:
        conn.close()


def execute(sql, args=()):
    conn = connect()
    try:
        with conn:
            return conn.execute(sql, args).lastrowid
    finally:
        conn.close()


def executemany(sql, seq):
    conn = connect()
    try:
        with conn:
            conn.executemany(sql, seq)
    finally:
        conn.close()
