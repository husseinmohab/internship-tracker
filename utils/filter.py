"""
utils/filter.py
Three hard gates — ALL must pass:
  1. No senior/staff/lead signal in title  (hard exclude, catches cached data too)
  2. Intern/student signal present in title
  3. Role keyword match
  4. Location is NYC-area, remote, or unspecified
  5. Date is after Aug 6 2026, or ambiguous
"""

import re
from datetime import date
from config import ROLE_KEYWORDS, START_DATE_SIGNALS, EXCLUDE_SIGNALS, START_AFTER


# ── Hard senior/full-time exclusion — checked on TITLE only ───────────────────
# If any of these appear in the title, job is rejected regardless of anything else.
_SENIOR_PATTERNS = re.compile(
    r"\b(senior|sr\.|staff|principal|lead|director|manager|head of|"
    r"vp |vice president|executive|partner|architect|"
    r"distinguished|fellow[^s]|c-suite|chief)\b",
    re.IGNORECASE,
)

# ── Intern / student signal — must appear in TITLE ────────────────────────────
_INTERN_PATTERNS = re.compile(
    r"\b(intern|internship|co-?op|student|reu|"
    r"undergraduate|grad student|research assistant|research associate|"
    r"part.?time|apprentice)\b",
    re.IGNORECASE,
)

# ── Location filter ────────────────────────────────────────────────────────────
_NYC_RE = re.compile(
    r"\b(new york|nyc|ny\b|manhattan|brooklyn|queens|bronx|staten island|"
    r"hoboken|jersey city|newark|princeton|stamford|connecticut|ct\b|"
    r"new jersey|nj\b|remote|hybrid|nationwide|multiple|various|usa|"
    r"united states)\b",
    re.IGNORECASE,
)

_NON_NYC_RE = re.compile(
    r"\b(san francisco|sf\b|seattle|austin|chicago|boston|denver|atlanta|"
    r"los angeles|la\b|dallas|houston|miami|phoenix|minneapolis|detroit|"
    r"charlotte|raleigh|pittsburgh|toronto|london|berlin|paris|bangalore|"
    r"hyderabad|singapore|sydney|dublin|canada|india|uk\b|bangalore)\b",
    re.IGNORECASE,
)


def classify_role(title: str, description: str = "") -> str | None:
    text = (title + " " + description).lower()
    for code, keywords in ROLE_KEYWORDS:
        for kw in keywords:
            if kw in text:
                return code
    return None


def has_senior_signal(title: str) -> bool:
    """True if title contains a senior/full-time signal — should be EXCLUDED."""
    return bool(_SENIOR_PATTERNS.search(title))


def has_intern_signal(title: str) -> bool:
    """True if title contains a student/intern signal — required to INCLUDE."""
    return bool(_INTERN_PATTERNS.search(title))


def passes_location(location: str) -> bool:
    if not location or not location.strip():
        return True  # unknown → keep
    if _NYC_RE.search(location):
        return True
    if _NON_NYC_RE.search(location):
        return False
    return True  # ambiguous → keep


def passes_date_filter(job: dict) -> str:
    parts = [
        job.get("title", ""),
        job.get("description", ""),
        job.get("start_date", ""),
        job.get("start_date_raw", ""),
    ]
    text = " ".join(p for p in parts if p).lower()

    for sig in EXCLUDE_SIGNALS:
        if sig in text:
            return "exclude"

    raw = job.get("start_date_raw", "")
    if raw:
        try:
            d = date.fromisoformat(raw[:10])
            cutoff = date.fromisoformat(START_AFTER)
            return "include" if d >= cutoff else "exclude"
        except ValueError:
            pass

    for sig in START_DATE_SIGNALS:
        if sig in text:
            return "include"

    return "maybe"


def passes_filter(job: dict) -> bool:
    title    = job.get("title", "").strip()
    desc     = job.get("description", "")
    location = job.get("location", "")
    source   = job.get("source", "")

    # 1. Must have a title
    if not title:
        return False

    # 2. Hard exclude: senior/staff/lead in title — no exceptions
    if has_senior_signal(title):
        return False

    # 3. Must match a role keyword
    role = classify_role(title, desc)
    if not role:
        return False

    # 4. Must have intern signal in title
    #    Exception: University source (research pages rarely say "intern")
    if source != "University" and not has_intern_signal(title):
        return False

    # 5. Location must be NYC-area, remote, or unknown
    if not passes_location(location):
        return False

    # 6. Date filter
    verdict = passes_date_filter(job)
    if verdict == "exclude":
        return False

    job["role"]            = role
    job["date_confidence"] = verdict
    return True
