# FuturePath — build progress

**Project:** FuturePath — a personalised career & stream guidance platform for Class 10+ students in India.
**Synopsis:** Dev Gupta (EN23CS301302), Divy Jain (EN23CS301342), Divyansh Choudhary (EN23CS301345)
**Guide:** Prof. Bhavna Tiwari · Medicaps University, Indore
**Location on disk:** `D:\FuturePath`
**Stack:** Python (Flask) backend · SQLite database · server-rendered frontend with vanilla JS

---

## What are the requirements and status for each

| # | requirement | Status |
|---|----------------------|--------|
| 1 | Student registration + academic record intake | ✅ |
| 2 | RIASEC interest inventory + skill self-assessment | ✅ |
| 3 | Relational database of students, assessments, and a knowledge base (careers, courses, colleges, exams, scholarships) | ✅ |
| 4 | Rule-based recommendation engine (profile → stream + careers) | ✅ |
| 5 | Exploration & comparison module (2–3 careers side by side) | ✅ |
| 6 | Step-by-step roadmap generation | ✅ |
| 7 | AI guidance chatbot for free-form questions | ⬜ |
| 8 | Single accessible, mobile-friendly UI | ✅ |
| 9 | Editorial redesign: imagery, dynamic sections, career explorer | ✅ |

✅ done · 🔄 in progress · ⬜ pending

---

## Build log

### Step 1 — Project scaffold and database schema
- Created `D:\FuturePath` with `app/`, `data/`, `content/`
- Wrote the full relational schema: students, academic records, assessment questions,
  assessment responses, streams, careers, courses, colleges, entrance exams, scholarships,
  recommendations, roadmaps

### Step 2 — Knowledge base content
- 6 streams after Class 10, each with subjects, who it suits, routes after, and an ideal
  RIASEC profile
- 12 careers profiled with day-in-the-life, required subjects, skills, salary bands, growth
  outlook and difficulty
- 17 courses, 14 colleges, 15 entrance exams (with eligibility, schedule, syllabus, prep
  time), 8 scholarships
- 34 assessment questions: 18 interest (3 per RIASEC dimension), 10 skill self-ratings,
  6 preference questions

### Step 3 — Recommendation engine
`app/engine.py`. Builds the student's profile from three signals — interest, skills and
subject marks — then scores every career with a weighted similarity, and aggregates stream
scores (a stream that opens several fitting careers ranks above one that leads to a single job).
Weights are declared in one place (`WEIGHTS`) so they can be tuned or replaced by a trained
model later without touching the algorithm.

Verified on a test profile (strong Investigative + Realistic, weak Artistic + Social):

| Rank | Career | Match |
|------|--------|-------|
| 1 | Software Engineer | 88.8% |
| 2 | Data Scientist / AI Engineer | 87.3% |
| 3 | Biotechnologist / Research Scientist | 86.5% |
| … | … | … |
| 10 | Designer | 66.6% |
| 12 | Entrepreneur | 59.5% |

Top stream: Science (PCM) at 94.8%. The ranking is sensible for that profile.

### Step 4 — Roadmap generation
`build_roadmap()` turns a chosen career into an ordered plan: stream decision → Class 11–12
subject focus → each entrance exam with its prep window → application strategy → matching
scholarships → what to do during the degree. Steps are tickable and saved per student.

### Step 5 — Content audit and correction
Audited every stream → career → exam mapping for correctness. Found and fixed five real errors:

1. **Data Scientist claimed Commerce as a route.** No Mathematics is assumed in the Commerce
   subject list, and the attached exams didn't line up. Now Science (PCM) only.
2. **Biotechnologist claimed NEET**, which is a medical entrance exam, not a biology-research
   one. Replaced with IISER Aptitude Test, CUET and NEST.
3. **Architect claimed JEE Main** without specifying the paper. B.Arch uses JEE Main **Paper 2**;
   added that as its own exam and attached NATA + Paper 2.
4. **Commerce was too thin** — only 4 careers. Added Company Secretary (with CSEET) and
   Investment / Financial Analyst, bringing it to 6 and matching what students actually ask about.
5. **Careers page ignored the `?stream=` filter** that the home page linked to, so "Careers from
   here" silently showed everything. Now filters correctly.

Also fixed a data-loss bug: `seed.py` was deleting and recreating the assessment questions, and
because `assessment_answers` has a foreign key onto them, reseeding wiped every student's
answers. Now upserted in place.

### Step 6 — Frontend
Eight pages: home, assessment, results, careers, career detail, comparison, exams &
scholarships, roadmap. Light, high-contrast, mobile-first — the audience is 15–16 year olds
on phones. Everything is inside the app; there are no outbound redirects.

### Step 7 — Editorial redesign
Rebuilt the presentation layer without touching any route, API, model or piece of
existing functionality.

- **Centralised image configuration** (`app/images.py`). 36 photographs, each pinned to a
  specific photo id with alt text and a credit, grouped as careers, streams, categories and
  editorial. `photo()` builds correctly sized, cropped, compressed URLs so a card downloads
  only the resolution it renders at. Every URL was verified to resolve; two dead ids were
  found and replaced. Nothing else in the codebase hardcodes an image URL.
- **Dynamic hero** with an orbital visual: three rotating rings, a floating FuturePath core,
  eight career nodes drifting on independent cycles, and pulsing data points. Pure CSS, GPU
  composited.
- **Circular profile progress ring** driven by real completion data, animated on scroll.
- **Rich career cards**: full-bleed image, gradient scrim, match percentage over the image,
  description, key skills, animated progress bar, and a hover state that zooms the image and
  lifts the card.
- **Visual roadmap**: six stages (goal → subjects → exams → courses → scholarships → skills)
  derived from the student's actual generated plan, with connector lines that light up as the
  section scrolls.
- **Discover your future**: horizontal, snap-scrolling category carousel with eight fields.
- **Career explorer** with animated field filtering on the home page.
- **Why FuturePath**: four numbered feature blocks with imagery.
- **Final CTA**: full-width gradient panel with the student's own next action.
- **Motion layer** (`app/static/js/fx.js`): aurora backdrop, staggered scroll reveals,
  count-up numbers, bars that fill on scroll, card tilt, progress rings, roadmap connectors
  and the filter logic — all in one place, all respecting `prefers-reduced-motion`.

### Verification
30 automated checks across auth, academics, assessment, profile, roadmap, every page and the
image audit. All passing. Highlights:

- register → login → save marks → answer assessment → results → roadmap → toggle step
- match percentages on the results page are computed from the student's own data
- every `<img>` has alt text; below-the-fold images are `loading="lazy"`, the two logos and the
  career hero are `fetchpriority="high"`

### Step 8 — Design refresh, theme support, subject manager

**Editorial restyle.** The first pass read as generic: 34 gradients, six frosted-glass layers,
43 shadows and a purple/teal/blue palette. Replaced with an editorial system — warm paper
background, navy ink, one accent colour used only for primary actions, hairline rules for
structure, and a serif display face against a system sans. Colour is now functional: green,
amber and red carry meaning; blue means "this is the action".

**Dark mode.** Every colour was already a CSS variable, so dark mode is a second set of token
values on `[data-theme="dark"]` — no component rule changes. Includes: a pre-paint script so a
dark-mode user never sees a white flash, persistence in `localStorage`, following the operating
system preference when the user has not chosen explicitly, a live sync if the OS setting changes
mid-session, and `color-scheme` so native form controls and scrollbars match.

**Navbar rebuilt.** Previously a wrapping flex row with no mobile treatment. Now a real
responsive bar: single row on desktop with the active page marked by a rule, and a hamburger
that opens a full-width sheet under 940px — animated icon, scroll lock, closes on link tap and
on Escape, with correct `aria-expanded` state.

**Students add their own subjects.** The fixed 14-subject list is gone. The assessment page now
has a subject manager: add a row with any subject name, type a percentage, remove with ×, tap
suggestions for common subjects (which disable themselves once used), live count, and validation
that names the offending subject. Verified with arbitrary names — *Astrophysics*,
*Marine Biology*, *Robotics & Automation* — all saved, edited and fed into the profile.

**Hero in motion.** The constellation was static. Each career node now rides a rotating carrier
while counter-rotating to stay upright: three rings at 34s / 26s / 19s, alternating direction, so
the composition never repeats. Added a rippling core, eight travelling spokes, hover labels
naming each career, and a rotating caption. Plus staggered card entry, 14px image parallax and a
match-score ticker across the rest of the page.

All motion is guarded by `prefers-reduced-motion`.

---

## How to run

```bash
cd D:\FuturePath
python seed.py      # first time: creates the database and loads the knowledge base
python run.py       # http://127.0.0.1:5001
```

## Notes

- The synopsis specifies PostgreSQL. This build uses SQLite so it runs with zero setup on
  any machine for the demo; the schema and queries are written so switching to PostgreSQL
  later is a connection-string change, not a rewrite.
- Everything the student needs is inside the app — no external redirects.
