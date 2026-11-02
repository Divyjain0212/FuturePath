"""Seed content: the RIASEC interest inventory, skill self-assessment, and the
knowledge base (streams, careers, courses, colleges, exams, scholarships).

Kept as data so the knowledge base can grow without touching application code.
"""

# ---------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------
# Likert 1..5 ("Strongly disagree" .. "Strongly agree") for interests, and
# 1..5 self-ratings for skills. Statements are written in the second person and
# anchored in things a 15-16 year old has actually experienced.

INTEREST_QUESTIONS = [
    # Realistic
    ("R", "I enjoy taking apart a device to understand how it works."),
    ("R", "I would rather build something with my hands than write about it."),
    ("R", "I like working outdoors or on machines, tools or equipment."),
    # Investigative
    ("I", "I enjoy solving puzzles or problems that take hours to figure out."),
    ("I", "I like asking 'why' until I understand how something actually works."),
    ("I", "I enjoy analysing data or evidence to find a pattern."),
    # Artistic
    ("A", "I enjoy drawing, designing, writing, music or making videos."),
    ("A", "I often come up with ideas nobody else in the room has thought of."),
    ("A", "I care about how things look and feel, not only whether they work."),
    # Social
    ("S", "I like explaining a difficult topic until someone finally understands it."),
    ("S", "People come to me when they need help or want to talk."),
    ("S", "I would find it satisfying to work directly with people who need support."),
    # Enterprising
    ("E", "I like being the one who organises a group and decides the plan."),
    ("E", "I enjoy convincing people of an idea I believe in."),
    ("E", "I would like to run something of my own one day."),
    # Conventional
    ("C", "I like having a clear process and following it properly."),
    ("C", "I am careful with details like records, accounts or schedules."),
    ("C", "I would rather work with organised information than with people all day."),
]

SKILL_QUESTIONS = [
    ("logical", "Working through a tricky maths or logic problem step by step."),
    ("creative", "Coming up with original ideas or designs."),
    ("communication", "Explaining something clearly, in writing or in person."),
    ("technical", "Using computers, software or technical tools."),
    ("numerical", "Working with numbers, statistics or calculations."),
    ("people", "Understanding how someone else is feeling and responding well."),
    ("organisation", "Keeping many tasks, deadlines and details in order."),
    ("leadership", "Taking charge of a group when something needs to get done."),
    ("hands_on", "Building, repairing or operating something physical."),
    ("research", "Finding reliable information and judging whether to trust it."),
]

PREFERENCE_QUESTIONS = [
    ("work_style", "I would prefer a job where the work is different every day."),
    ("people_contact", "I want a job with a lot of interaction with people."),
    ("risk", "I would be comfortable with an uncertain income if the work excited me."),
    ("stability", "Job security matters more to me than a high salary."),
    ("relocate", "I am willing to move to another city for the right course or job."),
    ("study_length", "I am happy to study for many years if the career needs it."),
]

LIKERT_LABELS = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly agree",
}

SKILL_LABELS = {
    1: "Not at all",
    2: "A little",
    3: "Moderate",
    4: "Good",
    5: "Very strong",
}


# ---------------------------------------------------------------------------
# Streams (Class 11 choices)
# ---------------------------------------------------------------------------
STREAMS = [
    {
        "slug": "science-pcm",
        "name": "Science (PCM)",
        "icon": "🔬",
        "summary": "Physics, Chemistry and Mathematics. The route into engineering, "
                   "architecture, technology and the physical sciences. Heavy on "
                   "problem-solving and mathematical reasoning.",
        "subjects": ["Physics", "Chemistry", "Mathematics", "English"],
        "who_it_suits": "Students who enjoy solving numerical problems, want to know how "
                        "things work, and are comfortable with a demanding workload. "
                        "If maths is a chore rather than a puzzle, think carefully.",
        "paths_after": ["B.Tech / B.E.", "B.Arch", "B.Sc (Physics/Maths/Statistics)",
                        "NDA / Defence", "Data Science", "Merchant Navy"],
        "riasec": {"R": 0.6, "I": 0.95, "A": 0.2, "S": 0.25, "E": 0.4, "C": 0.6},
        "sort_order": 10,
    },
    {
        "slug": "science-pcb",
        "name": "Science (PCB)",
        "icon": "🧬",
        "summary": "Physics, Chemistry and Biology. The route into medicine, "
                   "healthcare, life sciences and research. Requires long-term "
                   "commitment and strong memory plus reasoning.",
        "subjects": ["Physics", "Chemistry", "Biology", "English"],
        "who_it_suits": "Students genuinely interested in living systems and health, "
                        "who can sustain years of study. Choose it for the subject, not "
                        "for the prestige of the word 'doctor'.",
        "paths_after": ["MBBS", "BDS", "BAMS / BHMS", "B.Sc Nursing", "Pharmacy",
                        "Physiotherapy", "Biotechnology", "Veterinary Science"],
        "riasec": {"R": 0.5, "I": 0.9, "A": 0.2, "S": 0.7, "E": 0.25, "C": 0.6},
        "sort_order": 20,
    },
    {
        "slug": "science-pcmb",
        "name": "Science (PCMB)",
        "icon": "🧪",
        "summary": "All four: Physics, Chemistry, Mathematics and Biology. Keeps both "
                   "engineering and medicine open, at the cost of the heaviest workload "
                   "of any stream.",
        "subjects": ["Physics", "Chemistry", "Mathematics", "Biology"],
        "who_it_suits": "Students who are genuinely undecided between engineering and "
                        "medicine and are willing to carry a heavier load for one year. "
                        "Only worth it if you will actually use both doors.",
        "paths_after": ["Everything open to PCM and PCB", "Bioinformatics",
                        "Biomedical Engineering", "Research"],
        "riasec": {"R": 0.55, "I": 0.95, "A": 0.2, "S": 0.5, "E": 0.3, "C": 0.6},
        "sort_order": 30,
    },
    {
        "slug": "commerce",
        "name": "Commerce",
        "icon": "📈",
        "summary": "Accountancy, Business Studies, Economics and Mathematics or "
                   "Informatics. The route into finance, management, law and "
                   "entrepreneurship.",
        "subjects": ["Accountancy", "Business Studies", "Economics", "English",
                     "Mathematics (optional)"],
        "who_it_suits": "Students interested in how businesses, money and markets work. "
                        "Keep Mathematics if you can — it keeps B.Com (Hons), Economics "
                        "and data-heavy courses open.",
        "paths_after": ["B.Com / B.Com (Hons)", "BBA", "CA", "CS", "CMA",
                        "B.A. Economics", "Integrated Law (BBA-LLB)", "Actuarial Science"],
        "riasec": {"R": 0.2, "I": 0.6, "A": 0.25, "S": 0.5, "E": 0.9, "C": 0.9},
        "sort_order": 40,
    },
    {
        "slug": "humanities",
        "name": "Arts / Humanities",
        "icon": "📚",
        "summary": "History, Political Science, Psychology, Economics, Languages and "
                   "more. The widest stream — it leads to law, civil services, design, "
                   "media, psychology and academia.",
        "subjects": ["English", "History / Political Science", "Economics / Psychology",
                     "Elective of choice"],
        "who_it_suits": "Students who enjoy reading, arguing, writing and understanding "
                        "people and societies. Widely underestimated: it is the most "
                        "flexible stream for competitive exams and law.",
        "paths_after": ["B.A. (any subject)", "Integrated Law (BA-LLB)", "B.Des",
                        "Journalism & Mass Communication", "Psychology", "Civil Services",
                        "Social Work", "Economics"],
        "riasec": {"R": 0.15, "I": 0.7, "A": 0.8, "S": 0.9, "E": 0.6, "C": 0.5},
        "sort_order": 50,
    },
    {
        "slug": "vocational",
        "name": "Vocational / Skill-based",
        "icon": "🛠️",
        "summary": "Industry-linked courses such as IT, healthcare support, tourism, "
                   "automotive, beauty and wellness, or agriculture. Leads to early "
                   "employment, diplomas and lateral entry into degrees.",
        "subjects": ["Trade subject", "General subjects", "English", "IT / Soft skills"],
        "who_it_suits": "Students who learn best by doing, want to start earning sooner, "
                        "or plan to convert a skill into their own business. Not a "
                        "lesser route — it is a different one, and lateral entry into "
                        "degrees is available later.",
        "paths_after": ["Diploma / Polytechnic", "ITI to apprenticeship",
                        "B.Voc", "Lateral entry to B.Tech", "Self-employment"],
        "riasec": {"R": 0.9, "I": 0.35, "A": 0.5, "S": 0.5, "E": 0.6, "C": 0.5},
        "sort_order": 60,
    },
]


# ---------------------------------------------------------------------------
# Careers
# ---------------------------------------------------------------------------
CAREERS = [
    {
        "slug": "software-engineer",
        "name": "Software Engineer",
        "icon": "💻",
        "field": "Technology",
        "summary": "Designs, writes and maintains the software behind apps, websites, "
                   "and the systems companies run on. The work is part craft, part "
                   "problem-solving, and it changes every couple of years.",
        "day_in_life": "Stand-up with the team in the morning, then several hours of "
                       "focused coding, a code review for a colleague, and debugging "
                       "something that broke in production.",
        "skills": ["logical", "technical", "research", "organisation"],
        "subjects_needed": ["Mathematics", "Computer Science", "Physics"],
        "stream_slugs": ["science-pcm", "vocational"],
        "riasec": {"R": 0.5, "I": 0.95, "A": 0.4, "S": 0.3, "E": 0.4, "C": 0.7},
        "salary_start": "₹4–12 LPA (₹20 LPA+ at top product companies)",
        "salary_mid": "₹18–45 LPA",
        "growth": "Very strong — sustained demand, with AI changing what the work looks like rather than removing it.",
        "difficulty": "Moderate",
        "exams": ["jee-main", "jee-advanced", "bitsat"],
        "sort_order": 10,
    },
    {
        "slug": "data-scientist",
        "name": "Data Scientist / AI Engineer",
        "icon": "📊",
        "field": "Technology",
        "summary": "Finds patterns in data and builds models that predict or automate. "
                   "Sits between statistics, programming and the business problem being solved.",
        "day_in_life": "Cleaning a messy dataset, testing whether a model actually beats "
                       "the existing baseline, then explaining the result to a stakeholder "
                       "who does not care about the maths.",
        "skills": ["logical", "numerical", "research", "technical"],
        "subjects_needed": ["Mathematics", "Computer Science", "Statistics"],
        "stream_slugs": ["science-pcm"],
        "riasec": {"R": 0.3, "I": 0.98, "A": 0.35, "S": 0.4, "E": 0.45, "C": 0.8},
        "salary_start": "₹6–14 LPA",
        "salary_mid": "₹20–50 LPA",
        "growth": "Very strong, though the entry bar has risen — portfolios and projects now matter more than the degree name.",
        "difficulty": "High",
        "exams": ["jee-main", "cuet"],
        "sort_order": 20,
    },
    {
        "slug": "doctor",
        "name": "Doctor (MBBS)",
        "icon": "🩺",
        "field": "Healthcare",
        "summary": "Diagnoses and treats illness. One of the longest training routes in "
                   "India — five and a half years of MBBS, then specialisation — but "
                   "with unusual job security and social trust.",
        "day_in_life": "Morning rounds in the ward, outpatient consultations through the "
                       "afternoon, paperwork, and emergency calls that do not respect "
                       "your schedule.",
        "skills": ["logical", "people", "organisation", "research"],
        "subjects_needed": ["Biology", "Chemistry", "Physics"],
        "stream_slugs": ["science-pcb", "science-pcmb"],
        "riasec": {"R": 0.6, "I": 0.9, "A": 0.2, "S": 0.95, "E": 0.3, "C": 0.7},
        "salary_start": "₹6–12 LPA after MBBS",
        "salary_mid": "₹15–60 LPA depending on specialisation",
        "growth": "Steady and secure. Specialisation and location drive earnings far more than the initial degree.",
        "difficulty": "Very High",
        "exams": ["neet-ug"],
        "sort_order": 30,
    },
    {
        "slug": "chartered-accountant",
        "name": "Chartered Accountant",
        "icon": "🧾",
        "field": "Finance",
        "summary": "Audits accounts, files taxes and advises businesses on financial "
                   "decisions. Can be started right after Class 12 through the CA "
                   "Foundation route, without a degree first.",
        "day_in_life": "Reviewing ledgers for a client audit, checking a tax position "
                       "against the latest rules, and explaining a compliance risk to a "
                       "business owner.",
        "skills": ["numerical", "organisation", "logical", "communication"],
        "subjects_needed": ["Accountancy", "Mathematics", "Economics"],
        "stream_slugs": ["commerce"],
        "riasec": {"R": 0.2, "I": 0.7, "A": 0.15, "S": 0.45, "E": 0.7, "C": 0.98},
        "salary_start": "₹8–14 LPA on qualifying",
        "salary_mid": "₹20–60 LPA in practice or industry",
        "growth": "Strong. Pass rates are low, which is exactly why the qualification holds its value.",
        "difficulty": "High",
        "exams": ["ca-foundation"],
        "sort_order": 40,
    },
    {
        "slug": "designer",
        "name": "Designer (UX / Product / Graphic)",
        "icon": "🎨",
        "field": "Design & Media",
        "summary": "Shapes how a product looks, feels and works. UX designers decide "
                   "what a screen should do; graphic and communication designers shape "
                   "how a message looks.",
        "day_in_life": "Interviewing users about where an app confused them, sketching "
                       "three possible flows, then defending one of them in a review.",
        "skills": ["creative", "people", "communication", "research"],
        "subjects_needed": ["Fine Arts", "English", "Computer Science"],
        "stream_slugs": ["humanities", "science-pcm", "vocational"],
        "riasec": {"R": 0.3, "I": 0.6, "A": 0.98, "S": 0.7, "E": 0.55, "C": 0.4},
        "salary_start": "₹4–9 LPA",
        "salary_mid": "₹15–40 LPA",
        "growth": "Strong and portfolio-driven. Nobody asks your marks after your first job — they look at your work.",
        "difficulty": "Moderate",
        "exams": ["nid-dat", "uceed", "nift"],
        "sort_order": 50,
    },
    {
        "slug": "lawyer",
        "name": "Lawyer",
        "icon": "⚖️",
        "field": "Law",
        "summary": "Advises clients and argues cases, or works in corporate law on "
                   "contracts, mergers and compliance. The five-year integrated degree "
                   "can be started straight after Class 12.",
        "day_in_life": "Reading case files, drafting an argument, and appearing before a "
                       "court or negotiating a contract clause with the other side.",
        "skills": ["communication", "research", "logical", "people"],
        "subjects_needed": ["English", "Political Science", "History"],
        "stream_slugs": ["humanities", "commerce"],
        "riasec": {"R": 0.15, "I": 0.8, "A": 0.5, "S": 0.8, "E": 0.9, "C": 0.6},
        "salary_start": "₹5–15 LPA at a good firm",
        "salary_mid": "₹20–80 LPA in corporate practice",
        "growth": "Strong in corporate law; litigation takes longer to build but can be very rewarding.",
        "difficulty": "High",
        "exams": ["clat", "ailet"],
        "sort_order": 60,
    },
    {
        "slug": "company-secretary",
        "name": "Company Secretary",
        "icon": "📋",
        "field": "Finance",
        "summary": "The governance and compliance officer of a company — board meetings, "
                   "statutory filings, corporate law and advising directors on their duties.",
        "day_in_life": "Reviewing whether a board resolution is legally sound, filing "
                       "forms with the regulator before a deadline, and briefing directors "
                       "on a compliance risk.",
        "skills": ["organisation", "communication", "logical", "research"],
        "subjects_needed": ["Accountancy", "Business Studies", "Economics"],
        "stream_slugs": ["commerce"],
        "riasec": {"R": 0.15, "I": 0.7, "A": 0.15, "S": 0.55, "E": 0.6, "C": 0.98},
        "salary_start": "₹6–10 LPA on qualifying",
        "salary_mid": "₹15–40 LPA",
        "growth": "Steady. Every listed company must have one, which makes demand predictable "
                  "rather than cyclical.",
        "difficulty": "High",
        "exams": ["cseet"],
        "sort_order": 45,
    },
    {
        "slug": "financial-analyst",
        "name": "Investment / Financial Analyst",
        "icon": "📉",
        "field": "Finance",
        "summary": "Studies companies, markets and financial statements to decide where money "
                   "should go — in banking, asset management, equity research or corporate finance.",
        "day_in_life": "Building a model of a company's future earnings, testing it against "
                       "the assumptions, and writing up a recommendation someone will act on.",
        "skills": ["numerical", "logical", "research", "communication"],
        "subjects_needed": ["Mathematics", "Economics", "Accountancy"],
        "stream_slugs": ["commerce", "science-pcm"],
        "riasec": {"R": 0.15, "I": 0.9, "A": 0.2, "S": 0.4, "E": 0.75, "C": 0.9},
        "salary_start": "₹5–10 LPA",
        "salary_mid": "₹18–50 LPA",
        "growth": "Strong, but competitive. Certifications (CFA) and internships matter more "
                  "than the degree name.",
        "difficulty": "High",
        "exams": ["cuet"],
        "sort_order": 47,
    },
    {
        "slug": "civil-servant",
        "name": "Civil Servant (IAS/IPS/IFS)",
        "icon": "🏛️",
        "field": "Public Service",
        "summary": "Administers districts, departments or India's foreign missions. "
                   "Selected through the UPSC Civil Services Examination, which is open "
                   "to graduates of any stream.",
        "day_in_life": "Reviewing a development project, resolving a public grievance, "
                       "coordinating between departments, and being accountable for "
                       "decisions that affect thousands of people.",
        "skills": ["communication", "leadership", "organisation", "people"],
        "subjects_needed": ["English", "Political Science", "History", "Economics"],
        "stream_slugs": ["humanities", "commerce", "science-pcm", "science-pcb"],
        "riasec": {"R": 0.2, "I": 0.8, "A": 0.4, "S": 0.95, "E": 0.95, "C": 0.7},
        "salary_start": "₹10–12 LPA plus substantial benefits and authority",
        "salary_mid": "₹18–25 LPA at senior grades",
        "growth": "Prestige and impact rather than pure pay. Extremely competitive — roughly 1 in 1,000 clears it.",
        "difficulty": "Very High",
        "exams": ["upsc-cse"],
        "sort_order": 70,
    },
    {
        "slug": "entrepreneur",
        "name": "Entrepreneur / Business Owner",
        "icon": "🚀",
        "field": "Business",
        "summary": "Builds and runs a business — from a local service to a funded "
                   "startup. There is no entrance exam; the skills are learned by doing, "
                   "and the failure rate is high.",
        "day_in_life": "No two days are alike: talking to customers, fixing a cash-flow "
                       "problem, hiring, and deciding what to stop doing.",
        "skills": ["leadership", "communication", "people", "organisation"],
        "subjects_needed": ["Business Studies", "Economics", "Accountancy"],
        "stream_slugs": ["commerce", "vocational", "humanities", "science-pcm"],
        "riasec": {"R": 0.5, "I": 0.5, "A": 0.7, "S": 0.7, "E": 0.98, "C": 0.6},
        "salary_start": "Unpredictable — often nothing at first",
        "salary_mid": "Uncapped, and equally can be zero",
        "growth": "Highest variance of any option. Requires tolerance for uncertainty and for being wrong in public.",
        "difficulty": "Very High",
        "exams": [],
        "sort_order": 80,
    },
    {
        "slug": "biotechnologist",
        "name": "Biotechnologist / Research Scientist",
        "icon": "🧫",
        "field": "Science & Research",
        "summary": "Works in a lab on genetics, drug development, agriculture or "
                   "environmental science. Usually needs a master's or PhD for "
                   "independent research roles.",
        "day_in_life": "Running an experiment, analysing results, reading the latest "
                       "papers in the field, and documenting everything precisely.",
        "skills": ["logical", "research", "numerical", "organisation"],
        "subjects_needed": ["Biology", "Chemistry", "Mathematics"],
        "stream_slugs": ["science-pcb", "science-pcmb", "science-pcm"],
        "riasec": {"R": 0.7, "I": 0.98, "A": 0.3, "S": 0.35, "E": 0.2, "C": 0.85},
        "salary_start": "₹3–7 LPA after B.Sc",
        "salary_mid": "₹12–30 LPA with a PhD or in industry R&D",
        "growth": "Moderate in India, stronger abroad. A postgraduate degree is close to essential.",
        "difficulty": "High",
        "exams": ["iiser-aptitude", "cuet", "nest"],
        "sort_order": 90,
    },
    {
        "slug": "psychologist",
        "name": "Psychologist / Counsellor",
        "icon": "🧠",
        "field": "Healthcare",
        "summary": "Works with people on mental health, behaviour and learning. "
                   "Clinical practice needs a master's and supervised training; school "
                   "and career counselling needs less.",
        "day_in_life": "Sessions with clients, careful notes, supervision with a senior "
                       "practitioner, and continuing education to keep up with the field.",
        "skills": ["people", "communication", "research", "organisation"],
        "subjects_needed": ["Psychology", "Biology", "English"],
        "stream_slugs": ["humanities", "science-pcb"],
        "riasec": {"R": 0.15, "I": 0.8, "A": 0.55, "S": 0.98, "E": 0.4, "C": 0.6},
        "salary_start": "₹3–6 LPA",
        "salary_mid": "₹10–30 LPA in private practice",
        "growth": "Growing steadily as stigma reduces and school counselling expands. Private practice scales with reputation.",
        "difficulty": "Moderate",
        "exams": ["cuet"],
        "sort_order": 100,
    },
    {
        "slug": "architect",
        "name": "Architect",
        "icon": "🏛️",
        "field": "Design & Media",
        "summary": "Designs buildings and spaces that are safe, functional and "
                   "pleasant to be in. Requires a five-year B.Arch and registration "
                   "with the Council of Architecture.",
        "day_in_life": "Meeting a client about their brief, refining drawings and 3D "
                       "models, coordinating with structural engineers, and visiting site.",
        "skills": ["creative", "logical", "technical", "organisation"],
        "subjects_needed": ["Mathematics", "Physics", "Fine Arts"],
        "stream_slugs": ["science-pcm"],
        "riasec": {"R": 0.6, "I": 0.7, "A": 0.95, "S": 0.5, "E": 0.5, "C": 0.6},
        "salary_start": "₹3–8 LPA",
        "salary_mid": "₹12–35 LPA",
        "growth": "Moderate, tied to construction cycles. Strong specialisations in sustainable design and urban planning.",
        "difficulty": "High",
        "exams": ["nata", "jee-main-paper2"],
        "sort_order": 110,
    },
    {
        "slug": "journalist",
        "name": "Journalist / Content Creator",
        "icon": "🎙️",
        "field": "Design & Media",
        "summary": "Investigates and tells stories — in text, video or audio. The "
                   "traditional newsroom is shrinking while independent and digital "
                   "media is growing.",
        "day_in_life": "Chasing sources, verifying a claim before publishing it, writing "
                       "to a deadline, and defending your choices to an editor.",
        "skills": ["communication", "research", "creative", "people"],
        "subjects_needed": ["English", "History", "Political Science"],
        "stream_slugs": ["humanities"],
        "riasec": {"R": 0.2, "I": 0.8, "A": 0.9, "S": 0.8, "E": 0.75, "C": 0.4},
        "salary_start": "₹3–6 LPA",
        "salary_mid": "₹10–30 LPA for established independent creators",
        "growth": "Mixed in legacy media, strong for those who build their own audience.",
        "difficulty": "Moderate",
        "exams": ["cuet", "iimc"],
        "sort_order": 120,
    },
]


# ---------------------------------------------------------------------------
# Entrance exams
# ---------------------------------------------------------------------------
EXAMS = [
    {
        "slug": "jee-main",
        "name": "JEE Main",
        "full_name": "Joint Entrance Examination (Main)",
        "for_streams": ["science-pcm", "science-pcmb"],
        "eligibility": "Class 12 pass or appearing, with Physics, Chemistry and Mathematics",
        "when_held": "January and April each year (two attempts)",
        "window": "Applications open roughly 2 months before each session",
        "syllabus": ["Physics (Class 11–12)", "Chemistry (Class 11–12)", "Mathematics (Class 11–12)"],
        "prep_months": 24,
        "website": "jeemain.nta.nic.in",
    },
    {
        "slug": "jee-advanced",
        "name": "JEE Advanced",
        "full_name": "Joint Entrance Examination (Advanced)",
        "for_streams": ["science-pcm"],
        "eligibility": "Top ~2.5 lakh JEE Main qualifiers, and age/attempt limits apply",
        "when_held": "May or June",
        "window": "Registration opens after JEE Main results",
        "syllabus": ["Physics (advanced)", "Chemistry (advanced)", "Mathematics (advanced)"],
        "prep_months": 30,
        "website": "jeeadv.ac.in",
    },
    {
        "slug": "neet-ug",
        "name": "NEET UG",
        "full_name": "National Eligibility cum Entrance Test (Undergraduate)",
        "for_streams": ["science-pcb", "science-pcmb"],
        "eligibility": "Class 12 with Physics, Chemistry and Biology; minimum 50% for general category",
        "when_held": "May each year",
        "window": "Applications open around February",
        "syllabus": ["Physics", "Chemistry", "Biology (Botany and Zoology)"],
        "prep_months": 24,
        "website": "neet.nta.nic.in",
    },
    {
        "slug": "cuet",
        "name": "CUET UG",
        "full_name": "Common University Entrance Test (Undergraduate)",
        "for_streams": ["humanities", "commerce", "science-pcm", "science-pcb", "science-pcmb"],
        "eligibility": "Class 12 pass or appearing, any stream, for the chosen subjects",
        "when_held": "May–June",
        "window": "Applications open around February–March",
        "syllabus": ["General aptitude", "Domain subjects of your choice", "Language"],
        "prep_months": 8,
        "website": "cuet.samarth.ac.in",
    },
    {
        "slug": "clat",
        "name": "CLAT",
        "full_name": "Common Law Admission Test",
        "for_streams": ["humanities", "commerce", "science-pcm", "science-pcb"],
        "eligibility": "Class 12 with minimum 45% (40% for reserved categories)",
        "when_held": "December",
        "window": "Applications open around July–August",
        "syllabus": ["English", "Current affairs and general knowledge",
                     "Legal reasoning", "Logical reasoning", "Quantitative techniques"],
        "prep_months": 12,
        "website": "consortiumofnlus.ac.in",
    },
    {
        "slug": "nata",
        "name": "NATA",
        "full_name": "National Aptitude Test in Architecture",
        "for_streams": ["science-pcm"],
        "eligibility": "Class 12 with Mathematics, or a 10+3 diploma with Mathematics",
        "when_held": "Multiple sessions through the year",
        "window": "Check the official calendar for each session",
        "syllabus": ["Drawing and visual composition", "Mathematics", "General aptitude"],
        "prep_months": 12,
        "website": "nata.in",
    },
    {
        "slug": "nid-dat",
        "name": "NID DAT",
        "full_name": "National Institute of Design — Design Aptitude Test",
        "for_streams": ["humanities", "science-pcm", "vocational", "commerce"],
        "eligibility": "Class 12 pass or appearing, any stream",
        "when_held": "Prelims in December–January, mains in February–March",
        "window": "Applications open around September–October",
        "syllabus": ["Design aptitude", "Visualisation and drawing", "General awareness"],
        "prep_months": 12,
        "website": "nid.edu",
    },
    {
        "slug": "uceed",
        "name": "UCEED",
        "full_name": "Undergraduate Common Entrance Examination for Design (IITs)",
        "for_streams": ["science-pcm", "humanities", "vocational", "commerce"],
        "eligibility": "Class 12 pass or appearing, any stream",
        "when_held": "January",
        "window": "Applications open around October",
        "syllabus": ["Visualisation and spatial ability", "Observation and design sensitivity",
                     "Analytical and logical reasoning", "Design thinking"],
        "prep_months": 12,
        "website": "uceed.iitb.ac.in",
    },
    {
        "slug": "nift",
        "name": "NIFT Entrance",
        "full_name": "National Institute of Fashion Technology Entrance Exam",
        "for_streams": ["humanities", "vocational", "science-pcm", "commerce"],
        "eligibility": "Class 12 pass or appearing, any stream",
        "when_held": "February",
        "window": "Applications open around November–December",
        "syllabus": ["Creative ability", "General ability", "Situation test"],
        "prep_months": 12,
        "website": "nift.ac.in",
    },
    {
        "slug": "ca-foundation",
        "name": "CA Foundation",
        "full_name": "Chartered Accountancy Foundation Course (ICAI)",
        "for_streams": ["commerce"],
        "eligibility": "Class 12 pass; register with ICAI and complete a 4-month study period",
        "when_held": "Three sessions a year (January, May, September)",
        "window": "Register at least 4 months before the exam session",
        "syllabus": ["Accounting", "Business laws", "Quantitative aptitude", "Business economics"],
        "prep_months": 8,
        "website": "icai.org",
    },
    {
        "slug": "cseet",
        "name": "CSEET",
        "full_name": "Company Secretary Executive Entrance Test (ICSI)",
        "for_streams": ["commerce"],
        "eligibility": "Class 12 pass or appearing in any stream, with a minimum of 50%",
        "when_held": "Four sessions a year (January, May, July, November)",
        "window": "Register with ICSI roughly 2 months before the session",
        "syllabus": ["Business communication", "Legal aptitude and logical reasoning",
                     "Economics and business environment", "Current affairs"],
        "prep_months": 6,
        "website": "icsi.edu",
    },
    {
        "slug": "nest",
        "name": "NEST",
        "full_name": "National Entrance Screening Test (NISER and UM-DAE CEBS)",
        "for_streams": ["science-pcm", "science-pcb", "science-pcmb"],
        "eligibility": "Class 12 with science subjects, minimum 60% aggregate",
        "when_held": "May–June",
        "window": "Applications open around February–March",
        "syllabus": ["Biology", "Chemistry", "Mathematics", "Physics", "General ability"],
        "prep_months": 18,
        "website": "nestexam.in",
    },
    {
        "slug": "jee-main-paper2",
        "name": "JEE Main Paper 2 (B.Arch)",
        "full_name": "JEE Main Paper 2A — Bachelor of Architecture",
        "for_streams": ["science-pcm"],
        "eligibility": "Class 12 with Mathematics, or a 10+3 diploma with Mathematics",
        "when_held": "January and April, with JEE Main",
        "window": "Same application as JEE Main",
        "syllabus": ["Mathematics", "Aptitude test", "Drawing test"],
        "prep_months": 18,
        "website": "jeemain.nta.nic.in",
    },
    {
        "slug": "upsc-cse",
        "name": "UPSC Civil Services",
        "full_name": "Civil Services Examination (IAS, IPS, IFS and others)",
        "for_streams": ["humanities", "commerce", "science-pcm", "science-pcb", "science-pcmb"],
        "eligibility": "Any graduate; age 21–32 with category relaxations",
        "when_held": "Prelims in May–June, mains in September, interview in early next year",
        "window": "Applications open around February",
        "syllabus": ["General studies (history, polity, geography, economy, environment)",
                     "Aptitude", "Optional subject", "Essay", "Interview"],
        "prep_months": 18,
        "website": "upsc.gov.in",
    },
    {
        "slug": "bitsat",
        "name": "BITSAT",
        "full_name": "BITS Admission Test",
        "for_streams": ["science-pcm"],
        "eligibility": "Class 12 with minimum 75% aggregate in Physics, Chemistry and Mathematics",
        "when_held": "May–June",
        "window": "Applications open around January",
        "syllabus": ["Physics", "Chemistry", "Mathematics", "English", "Logical reasoning"],
        "prep_months": 18,
        "website": "bitsadmission.com",
    },
    {
        "slug": "ailet",
        "name": "AILET",
        "full_name": "All India Law Entrance Test (NLU Delhi)",
        "for_streams": ["humanities", "commerce", "science-pcm", "science-pcb"],
        "eligibility": "Class 12 with minimum 50%",
        "when_held": "December",
        "window": "Applications open around August",
        "syllabus": ["English", "Current affairs", "Logical reasoning", "Legal aptitude"],
        "prep_months": 10,
        "website": "nationallawuniversitydelhi.in",
    },
    {
        "slug": "iiser-aptitude",
        "name": "IISER Aptitude Test",
        "full_name": "Indian Institutes of Science Education and Research Aptitude Test",
        "for_streams": ["science-pcm", "science-pcb", "science-pcmb"],
        "eligibility": "Class 12 in the science stream",
        "when_held": "May–June",
        "window": "Applications open around March",
        "syllabus": ["Biology", "Chemistry", "Mathematics", "Physics"],
        "prep_months": 18,
        "website": "iiseradmission.in",
    },
    {
        "slug": "iimc",
        "name": "IIMC Entrance",
        "full_name": "Indian Institute of Mass Communication Entrance Examination",
        "for_streams": ["humanities", "commerce", "science-pcm"],
        "eligibility": "Bachelor's degree in any discipline",
        "when_held": "May–June",
        "window": "Applications open around March",
        "syllabus": ["General awareness", "English", "Reasoning", "Subject-specific"],
        "prep_months": 6,
        "website": "iimc.gov.in",
    },
]


# ---------------------------------------------------------------------------
# Scholarships
# ---------------------------------------------------------------------------
SCHOLARSHIPS = [
    {
        "slug": "nsp-pre-matric",
        "name": "National Scholarship Portal — Pre-Matric",
        "provider": "Government of India",
        "amount": "Varies by class and category",
        "eligibility": "Class 9–10 students from SC/ST/OBC/minority families within income limits",
        "for_streams": [],
        "deadline": "Usually October–November",
        "notes": "Apply through the National Scholarship Portal. One application covers several schemes.",
    },
    {
        "slug": "nsp-post-matric",
        "name": "National Scholarship Portal — Post-Matric",
        "provider": "Government of India",
        "amount": "Tuition support plus maintenance allowance",
        "eligibility": "Class 11 onwards for SC/ST/OBC/minority students within the family income limit",
        "for_streams": [],
        "deadline": "Usually October–November",
        "notes": "Most underused large scholarship in India — the eligibility is broader than students assume.",
    },
    {
        "slug": "inspire-scholarship",
        "name": "INSPIRE Scholarship (SHE)",
        "provider": "Department of Science and Technology",
        "amount": "₹80,000 per year",
        "eligibility": "Top 1% in Class 12 board exams, pursuing B.Sc/M.Sc in natural sciences",
        "for_streams": ["science-pcm", "science-pcb", "science-pcmb"],
        "deadline": "Usually July–August",
        "notes": "For students choosing pure science over engineering — a genuine alternative funding route.",
    },
    {
        "slug": "kvpy-merged",
        "name": "Merit-based Institute Scholarships",
        "provider": "Various IITs, NITs and universities",
        "amount": "Tuition waiver or stipend, varies",
        "eligibility": "Merit rank within the institute, often with an income condition",
        "for_streams": ["science-pcm", "science-pcb"],
        "deadline": "Check with the institute after admission",
        "notes": "Many students never check. Ask the institute's scholarship cell in your first week.",
    },
    {
        "slug": "pragati",
        "name": "AICTE Pragati Scholarship (for girls)",
        "provider": "AICTE",
        "amount": "₹50,000 per year",
        "eligibility": "Girl students in AICTE-approved technical degree or diploma programmes",
        "for_streams": ["science-pcm", "vocational"],
        "deadline": "Usually October–November",
        "notes": "Two girls per family are eligible. Covers tuition and incidental costs.",
    },
    {
        "slug": "saksham",
        "name": "AICTE Saksham Scholarship (for differently-abled)",
        "provider": "AICTE",
        "amount": "₹50,000 per year",
        "eligibility": "Students with 40%+ disability in AICTE-approved technical programmes",
        "for_streams": ["science-pcm", "vocational"],
        "deadline": "Usually October–November",
        "notes": "Applied through the National Scholarship Portal alongside other schemes.",
    },
    {
        "slug": "state-scholarships",
        "name": "State Government Scholarships",
        "provider": "Respective state governments",
        "amount": "Varies widely by state",
        "eligibility": "Domicile requirements, category and income limits vary by state",
        "for_streams": [],
        "deadline": "Varies — check your state portal",
        "notes": "Often more generous than central schemes and much less competitive. Always check your own state first.",
    },
    {
        "slug": "reliance-foundation",
        "name": "Reliance Foundation Undergraduate Scholarship",
        "provider": "Reliance Foundation",
        "amount": "Up to ₹2,00,000 over the degree",
        "eligibility": "First-year undergraduates across disciplines, merit plus means assessed",
        "for_streams": [],
        "deadline": "Usually September–October",
        "notes": "Open to all streams and one of the larger private scholarships available.",
    },
]


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------
COURSES = [
    {"slug": "btech-cse", "name": "B.Tech Computer Science & Engineering", "level": "Undergraduate",
     "duration": "4 years", "stream_slug": "science-pcm",
     "summary": "Programming, algorithms, systems, databases and networks, with electives in AI, security or distributed systems.",
     "careers": ["software-engineer", "data-scientist"]},
    {"slug": "btech-mech", "name": "B.Tech Mechanical Engineering", "level": "Undergraduate",
     "duration": "4 years", "stream_slug": "science-pcm",
     "summary": "Design, thermodynamics, manufacturing and robotics. Feeds into core industry, automotive and aerospace.",
     "careers": ["software-engineer", "entrepreneur"]},
    {"slug": "barch", "name": "Bachelor of Architecture", "level": "Undergraduate",
     "duration": "5 years", "stream_slug": "science-pcm",
     "summary": "Building design, structures, materials and urban planning, with studio work throughout.",
     "careers": ["architect", "designer"]},
    {"slug": "mbbs", "name": "MBBS", "level": "Undergraduate",
     "duration": "5.5 years including internship", "stream_slug": "science-pcb",
     "summary": "Medicine and surgery. Followed by internship and, usually, a specialisation.",
     "careers": ["doctor", "biotechnologist"]},
    {"slug": "bds", "name": "Bachelor of Dental Surgery", "level": "Undergraduate",
     "duration": "5 years", "stream_slug": "science-pcb",
     "summary": "Dentistry, oral surgery and orthodontics, with clinical practice built in.",
     "careers": ["doctor"]},
    {"slug": "bsc-nursing", "name": "B.Sc Nursing", "level": "Undergraduate",
     "duration": "4 years", "stream_slug": "science-pcb",
     "summary": "Clinical care, patient management and public health. Strong demand in India and abroad.",
     "careers": ["doctor", "psychologist"]},
    {"slug": "bpharm", "name": "Bachelor of Pharmacy", "level": "Undergraduate",
     "duration": "4 years", "stream_slug": "science-pcb",
     "summary": "Drug formulation, pharmacology and regulatory affairs. Feeds pharma manufacturing and R&D.",
     "careers": ["biotechnologist"]},
    {"slug": "bsc-biotech", "name": "B.Sc Biotechnology", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "science-pcb",
     "summary": "Genetics, molecular biology and bioprocessing. Usually continued to a master's for research roles.",
     "careers": ["biotechnologist", "data-scientist"]},
    {"slug": "bcom-hons", "name": "B.Com (Hons)", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "commerce",
     "summary": "Accounting, finance, taxation and business law, with a research or specialisation track.",
     "careers": ["chartered-accountant", "entrepreneur"]},
    {"slug": "bba", "name": "Bachelor of Business Administration", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "commerce",
     "summary": "Management, marketing, operations and human resources, often with internships each year.",
     "careers": ["entrepreneur", "chartered-accountant"]},
    {"slug": "ba-economics", "name": "B.A. Economics", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "commerce",
     "summary": "Micro and macroeconomics, econometrics and development economics. A strong route into policy and analytics.",
     "careers": ["data-scientist", "civil-servant"]},
    {"slug": "ba-llb", "name": "B.A. LL.B (Integrated Law)", "level": "Undergraduate",
     "duration": "5 years", "stream_slug": "humanities",
     "summary": "Law combined with humanities, with moot courts and internships from the second year.",
     "careers": ["lawyer", "civil-servant"]},
    {"slug": "ba-psychology", "name": "B.A. / B.Sc Psychology", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "humanities",
     "summary": "Cognition, development, clinical and social psychology. Clinical practice needs a master's.",
     "careers": ["psychologist"]},
    {"slug": "bdes", "name": "Bachelor of Design", "level": "Undergraduate",
     "duration": "4 years", "stream_slug": "humanities",
     "summary": "Product, communication, interaction or fashion design, taught largely through studio projects.",
     "careers": ["designer"]},
    {"slug": "bjmc", "name": "B.A. Journalism & Mass Communication", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "humanities",
     "summary": "Reporting, editing, media law and digital production, with newsroom internships.",
     "careers": ["journalist"]},
    {"slug": "bvoc", "name": "B.Voc (Bachelor of Vocation)", "level": "Undergraduate",
     "duration": "3 years", "stream_slug": "vocational",
     "summary": "Skill-based degree with exit points at one year (diploma) and two years (advanced diploma).",
     "careers": ["entrepreneur", "software-engineer"]},
    {"slug": "polytechnic-diploma", "name": "Polytechnic Diploma (Engineering)", "level": "Diploma",
     "duration": "3 years", "stream_slug": "vocational",
     "summary": "Practical engineering technician training, with lateral entry into the second year of B.Tech.",
     "careers": ["software-engineer", "entrepreneur"]},
]


# ---------------------------------------------------------------------------
# Colleges (illustrative, drawn from well-known institutions)
# ---------------------------------------------------------------------------
COLLEGES = [
    {"slug": "iit-bombay", "name": "Indian Institute of Technology Bombay", "city": "Mumbai",
     "state": "Maharashtra", "type": "Government",
     "courses": ["btech-cse", "btech-mech"], "entrance_exams": ["jee-advanced"],
     "notes": "India's top-ranked engineering institute. Strong placement and research culture.",
     "website": "iitb.ac.in"},
    {"slug": "iit-delhi", "name": "Indian Institute of Technology Delhi", "city": "New Delhi",
     "state": "Delhi", "type": "Government",
     "courses": ["btech-cse", "btech-mech"], "entrance_exams": ["jee-advanced"],
     "notes": "Strong in computer science and design (UCEED also runs here).",
     "website": "iitd.ac.in"},
    {"slug": "aiims-delhi", "name": "All India Institute of Medical Sciences", "city": "New Delhi",
     "state": "Delhi", "type": "Government",
     "courses": ["mbbs", "bsc-nursing"], "entrance_exams": ["neet-ug"],
     "notes": "Premier medical institute. Fees are unusually low and demand correspondingly high.",
     "website": "aiims.edu"},
    {"slug": "cmc-vellore", "name": "Christian Medical College", "city": "Vellore",
     "state": "Tamil Nadu", "type": "Private",
     "courses": ["mbbs", "bsc-nursing"], "entrance_exams": ["neet-ug"],
     "notes": "Well-regarded for clinical training and community medicine.",
     "website": "cmch-vellore.edu"},
    {"slug": "srcc", "name": "Shri Ram College of Commerce", "city": "New Delhi",
     "state": "Delhi", "type": "Government",
     "courses": ["bcom-hons", "ba-economics"], "entrance_exams": ["cuet"],
     "notes": "One of the most competitive commerce colleges in the country.",
     "website": "srcc.edu"},
    {"slug": "nls-bangalore", "name": "National Law School of India University", "city": "Bengaluru",
     "state": "Karnataka", "type": "Government",
     "courses": ["ba-llb"], "entrance_exams": ["clat"],
     "notes": "The first National Law University, and consistently the most sought after.",
     "website": "nls.ac.in"},
    {"slug": "nlu-delhi", "name": "National Law University Delhi", "city": "New Delhi",
     "state": "Delhi", "type": "Government",
     "courses": ["ba-llb"], "entrance_exams": ["ailet"],
     "notes": "Admits through its own AILET examination.",
     "website": "nludelhi.ac.in"},
    {"slug": "nid-ahmedabad", "name": "National Institute of Design", "city": "Ahmedabad",
     "state": "Gujarat", "type": "Government",
     "courses": ["bdes"], "entrance_exams": ["nid-dat"],
     "notes": "India's foremost design institute; portfolio and studio work dominate the course.",
     "website": "nid.edu"},
    {"slug": "nift-delhi", "name": "National Institute of Fashion Technology", "city": "New Delhi",
     "state": "Delhi", "type": "Government",
     "courses": ["bdes"], "entrance_exams": ["nift"],
     "notes": "Fashion, textile and communication design with strong industry links.",
     "website": "nift.ac.in"},
    {"slug": "iisermohali", "name": "IISER Mohali", "city": "Mohali",
     "state": "Punjab", "type": "Government",
     "courses": ["bsc-biotech"], "entrance_exams": ["iiser-aptitude"],
     "notes": "Research-focused science education with an integrated master's route.",
     "website": "iisermohali.ac.in"},
    {"slug": "symbiosis-pune", "name": "Symbiosis International University", "city": "Pune",
     "state": "Maharashtra", "type": "Private",
     "courses": ["bba", "bcom-hons"], "entrance_exams": ["cuet"],
     "notes": "Large private university with a broad management and design portfolio.",
     "website": "siu.edu.in"},
    {"slug": "jain-university", "name": "Jain (Deemed-to-be) University", "city": "Bengaluru",
     "state": "Karnataka", "type": "Deemed",
     "courses": ["btech-cse", "bba", "bdes"], "entrance_exams": [],
     "notes": "Admits on board marks plus its own assessment; broad programme choice.",
     "website": "jainuniversity.ac.in"},
    {"slug": "medicaps", "name": "Medicaps University", "city": "Indore",
     "state": "Madhya Pradesh", "type": "Private",
     "courses": ["btech-cse", "bba", "bpharm"], "entrance_exams": [],
     "notes": "Admits through state counselling and its own process; strong regional placement.",
     "website": "medicaps.ac.in"},
    {"slug": "davv", "name": "Devi Ahilya Vishwavidyalaya", "city": "Indore",
     "state": "Madhya Pradesh", "type": "Government",
     "courses": ["bcom-hons", "bsc-biotech", "ba-psychology"], "entrance_exams": [],
     "notes": "Large state university with a wide range of undergraduate programmes.",
     "website": "dauniv.ac.in"},
]
