"""Centralised image configuration.

Every image used anywhere in the UI is declared here, once, with alt text and a
`kind` so the layout knows how to size it. Nothing else in the codebase hardcodes
an image URL — to change the visual identity, edit this file only.

Why remote URLs (Unsplash):
  * the repository stays small and there are no binary assets to manage,
  * images are served from a CDN with responsive resizing,
  * each entry pins a specific photo, so the same career always shows the same
    picture rather than a random one from a search.

`photo()` builds a properly sized, cropped, compressed URL for a given width, so
cards can request exactly the resolution they render at (and a 2x variant for
retina) instead of downloading one oversized file.

Attribution: Unsplash photos are free to use under the Unsplash License
(https://unsplash.com/license). The photographer is recorded per image so the
project can credit them if a page footer is added later.
"""
from urllib.parse import quote

# Base params that apply to every request: auto format (webp/avif), quality, and
# a crop that keeps the subject centred.
_BASE = "auto=format&fit=crop&q=72"


def photo(photo_id, width=900, height=600, gravity="center"):
    """Build a responsive Unsplash URL for a pinned photo id."""
    return (f"https://images.unsplash.com/photo-{photo_id}"
            f"?{_BASE}&w={width}&h={height}&crop=entropy&cs=tinysrgb&fit=crop"
            f"&ixlib=rb-4.0.3&q=72&auto=format")


# ---------------------------------------------------------------------------
# Careers — one image per career, chosen to communicate the actual work.
# ---------------------------------------------------------------------------
CAREER_IMAGES = {
    "software-engineer": {
        "id": "1461749280684-dccba630e2f6",
        "alt": "Developer writing code on a laptop with source code on screen",
        "credit": "Christopher Gower",
    },
    "data-scientist": {
        "id": "1555949963-aa79dcee981c",
        "alt": "Data and machine-learning analysis shown on a computer screen",
        "credit": "Markus Spiske",
    },
    "doctor": {
        "id": "1576091160399-112ba8d25d1d",
        "alt": "Doctor in a white coat examining a patient's scan",
        "credit": "National Cancer Institute",
    },
    "chartered-accountant": {
        "id": "1554224155-6726b3ff858f",
        "alt": "Financial statements, calculator and pen on a desk",
        "credit": "Kelly Sikkema",
    },
    "company-secretary": {
        "id": "1450101499163-c8848c66ca85",
        "alt": "Documents and legal paperwork being reviewed at a desk",
        "credit": "Helloquence",
    },
    "financial-analyst": {
        "id": "1611974789855-9c2a0a7236a3",
        "alt": "Stock market charts displayed on a trading screen",
        "credit": "Maxim Hopman",
    },
    "designer": {
        "id": "1561070791-2526d30994b5",
        "alt": "Designer sketching interface layouts on a tablet",
        "credit": "UX Store",
    },
    "lawyer": {
        "id": "1589829545856-d10d557cf95f",
        "alt": "Law books and a gavel on a desk in a legal library",
        "credit": "Tingey Injury Law Firm",
    },
    "civil-servant": {
        "id": "1529107386315-e1a2ed48a620",
        "alt": "Government building with columns and steps",
        "credit": "Sebastian Pichler",
    },
    "entrepreneur": {
        "id": "1556761175-b413da4baf72",
        "alt": "Startup team collaborating in a bright office",
        "credit": "Austin Distel",
    },
    "biotechnologist": {
        "id": "1532187863486-abf9dbad1b69",
        "alt": "Researcher pipetting samples in a life-sciences laboratory",
        "credit": "National Cancer Institute",
    },
    "psychologist": {
        "id": "1573497491765-dccce02b29df",
        "alt": "Counsellor listening to a client in a calm consulting room",
        "credit": "Christina @ wocintechchat",
    },
    "architect": {
        "id": "1503387762-592deb58ef4e",
        "alt": "Architect working on building plans and models",
        "credit": "Daniel McCullough",
    },
    "journalist": {
        "id": "1504711434969-e33886168f5c",
        "alt": "Journalist writing at a desk with newspapers and a camera",
        "credit": "AbsolutVision",
    },
}

# ---------------------------------------------------------------------------
# Streams — Class 11 choices.
# ---------------------------------------------------------------------------
STREAM_IMAGES = {
    "science-pcm": {
        "id": "1635070041078-e363dbe005cb",
        "alt": "Physics and mathematics equations written on a blackboard",
        "credit": "Dan Cristian Padure",
    },
    "science-pcb": {
        "id": "1576086213369-97a306d36557",
        "alt": "Biology laboratory with microscopes and specimens",
        "credit": "National Cancer Institute",
    },
    "science-pcmb": {
        "id": "1582719508461-905c673771fd",
        "alt": "Science laboratory bench with glassware and instruments",
        "credit": "Hans Reniers",
    },
    "commerce": {
        "id": "1454165804606-c3d57bc86b40",
        "alt": "Business charts and financial analysis on a desk",
        "credit": "Carlos Muza",
    },
    "humanities": {
        "id": "1481627834876-b7833e8f5570",
        "alt": "Shelves of books in a library reading room",
        "credit": "Janko Ferlic",
    },
    "vocational": {
        "id": "1581092918056-0c4c3acd3789",
        "alt": "Trainee working with tools on a technical project",
        "credit": "ThisisEngineering",
    },
}

# ---------------------------------------------------------------------------
# Category banners — the "Discover your future" horizontal carousel.
# ---------------------------------------------------------------------------
CATEGORY_IMAGES = {
    "Technology": {
        "id": "1518770660439-4636190af475",
        "alt": "Circuit board and computing hardware close-up",
        "credit": "Umberto",
    },
    "Healthcare": {
        "id": "1631217868264-e5b90bb7e133",
        "alt": "Medical team working together in a hospital corridor",
        "credit": "Piron Guillaume",
    },
    "Science & Research": {
        "id": "1560472354-b33ff0c44a43",
        "alt": "Scientist examining samples in a research laboratory",
        "credit": "ThisisEngineering",
    },
    "Business": {
        "id": "1552664730-d307ca884978",
        "alt": "Team meeting around a table discussing a business plan",
        "credit": "Austin Distel",
    },
    "Design & Media": {
        "id": "1561070791-2526d30994b5",
        "alt": "Designers reviewing colour swatches and layouts",
        "credit": "UX Store",
    },
    "Finance": {
        "id": "1590283603385-17ffb3a7f29f",
        "alt": "Financial analyst reviewing market data on screens",
        "credit": "Nick Chong",
    },
    "Law": {
        "id": "1589578527966-fdac0f44566c",
        "alt": "Scales of justice and law books on a desk",
        "credit": "Tingey Injury Law Firm",
    },
    "Public Service": {
        "id": "1529107386315-e1a2ed48a620",
        "alt": "Civic building with classical columns",
        "credit": "Sebastian Pichler",
    },
}

# ---------------------------------------------------------------------------
# Mentors — shown inside the hero constellation.
#
# These are generic young professionals, presented as "a mentor", never as a
# named or real individual. Attribution is recorded so the project can credit
# the photographers if a credits page is added later.
# ---------------------------------------------------------------------------
MENTOR_IMAGES = [
    {
        "id": "1507003211169-0a1dd7228f2d",
        "alt": "A mentor smiling, presented as an illustration of guidance",
        "credit": "Joseph Gonzalez",
        "focus": "50% 28%",
    },
    {
        "id": "1494790108377-be9c29b29330",
        "alt": "A mentor smiling, presented as an illustration of guidance",
        "credit": "Michael Dam",
        "focus": "50% 26%",
    },
    {
        "id": "1519345182560-3f2917c472ef",
        "alt": "A mentor smiling, presented as an illustration of guidance",
        "credit": "Foto Sushi",
        "focus": "50% 26%",
    },
    {
        "id": "1544005313-94ddf0286df2",
        "alt": "A mentor smiling, presented as an illustration of guidance",
        "credit": "Christopher Campbell",
        "focus": "50% 26%",
    },
]


def mentor_count():
    return len(MENTOR_IMAGES)


def mentor_image(index, width=520, height=640):
    """Return one of the mentor portraits, chosen by index (rotates per render)."""
    entry = MENTOR_IMAGES[index % len(MENTOR_IMAGES)]
    return {
        "url": photo(entry["id"], width, height),
        "alt": entry["alt"],
        "credit": entry["credit"],
        "focus": entry.get("focus", "50% 30%"),
        "count": len(MENTOR_IMAGES),
    }


# ---------------------------------------------------------------------------
# Editorial and feature imagery.
# ---------------------------------------------------------------------------
EDITORIAL_IMAGES = {
    "students": {
        "id": "1523240795612-9a054b0db644",
        "alt": "Students studying together with notebooks and a laptop",
        "credit": "Alexis Brown",
    },
    "collaboration": {
        "id": "1522071820081-009f0129c71c",
        "alt": "Team of young professionals collaborating around a laptop",
        "credit": "Annie Spratt",
    },
    "mentor": {
        "id": "1571260899304-425eee4c7efc",
        "alt": "Mentor guiding a student through a project",
        "credit": "ThisisEngineering",
    },
    "coding": {
        "id": "1498050108023-c5249f4df085",
        "alt": "Laptop showing code in a development environment",
        "credit": "Christopher Gower",
    },
    "lab": {
        "id": "1582719478250-c89cae4dc85b",
        "alt": "Researcher at a laboratory bench with scientific equipment",
        "credit": "Hans Reniers",
    },
    "design-studio": {
        "id": "1558655146-9f40138edfeb",
        "alt": "Design studio workspace with sketches and screens",
        "credit": "Balazs Ketyi",
    },
    "graduation": {
        "id": "1541339907198-e08756dedf3f",
        "alt": "Graduates celebrating at a university convocation",
        "credit": "Vasily Koloda",
    },
    "future": {
        "id": "1451187580459-43490279c0fa",
        "alt": "Abstract network of connected light points representing technology",
        "credit": "NASA",
    },
}


# ---------------------------------------------------------------------------
# Helpers used by the templates.
# ---------------------------------------------------------------------------
def career_image(slug, width=800, height=560):
    entry = CAREER_IMAGES.get(slug)
    if not entry:
        return {"url": "", "alt": "", "credit": ""}
    return {
        "url": photo(entry["id"], width, height),
        "alt": entry["alt"],
        "credit": entry["credit"],
    }


def stream_image(slug, width=800, height=520):
    entry = STREAM_IMAGES.get(slug)
    if not entry:
        return {"url": "", "alt": "", "credit": ""}
    return {
        "url": photo(entry["id"], width, height),
        "alt": entry["alt"],
        "credit": entry["credit"],
    }


def category_image(field, width=700, height=880):
    entry = CATEGORY_IMAGES.get(field)
    if not entry:
        return {"url": "", "alt": "", "credit": ""}
    return {
        "url": photo(entry["id"], width, height),
        "alt": entry["alt"],
        "credit": entry["credit"],
    }


def editorial_image(key, width=1000, height=700):
    entry = EDITORIAL_IMAGES.get(key)
    if not entry:
        return {"url": "", "alt": "", "credit": ""}
    return {
        "url": photo(entry["id"], width, height),
        "alt": entry["alt"],
        "credit": entry["credit"],
    }


def cover_for(slug):
    """Pick the best banner image for a career, falling back to its field."""
    entry = CAREER_IMAGES.get(slug)
    if entry:
        return photo(entry["id"], 1200, 600)
    return photo(EDITORIAL_IMAGES["students"]["id"], 1200, 600)
