"""
utils/filter.py
Decides whether a normalized job dict is relevant.

Three hard requirements — ALL must pass:
  1. Role match    — title or description contains a relevant role keyword
  2. Intern signal — title must contain an intern/co-op/research signal
                     (prevents full-time senior roles from slipping through)
  3. Date filter   — start date after Aug 6 2026, or ambiguous
  4. Location      — must be NYC-area, remote, or unspecified
"""

import re
from datetime import date
from config import ROLE_KEYWORDS, START_DATE_SIGNALS, EXCLUDE_SIGNALS, START_AFTER


# ── Intern / student signal ────────────────────────────────────────────────────
# At least one of these must appear in the TITLE for a job to be kept.
# This is the primary guard against full-time roles.
_INTERN_PATTERNS = re.compile(
    r"\b(intern|internship|co-?op|student|reu|fellowship|fellow|"
    r"undergraduate|grad student|research assistant|research associate|"
    r"part.?time|apprentice)\b",
    re.IGNORECASE,
)

# ── Location: NYC-area or acceptable ──────────────────────────────────────────
# Jobs are kept if they match NYC/NJ/CT area, are remote, or have no location.
# Jobs with a clear non-NYC US city are excluded.
_NYC_RE = re.compile(
    r"\b(new york|nyc|ny\b|manhattan|brooklyn|queens|bronx|staten island|"
    r"hoboken|jersey city|newark|princeton|stamford|connecticut|ct\b|"
    r"new jersey|nj\b|remote|hybrid|nationwide|multiple|various|usa|"
    r"united states)\b",
    re.IGNORECASE,
)

# Cities that are clearly NOT NYC-area — exclude if matched and no NYC signal
_NON_NYC_RE = re.compile(
    r"\b(san francisco|sf\b|seattle|austin|chicago|boston|denver|atlanta|"
    r"los angeles|la\b|dallas|houston|miami|phoenix|minneapolis|detroit|"
    r"charlotte|raleigh|pittsburgh|toronto|london|berlin|paris|bangalore|"
    r"hyderabad|singapore|sydney|dublin)\b",
    re.IGNORECASE,
)


def classify_role(title: str, description: str = "") -> str | None:
    """Return role code (de/da/ds/swe/re/ra) or None if no match."""
    text = (title + " " + description).lower()
    for code, keywords in ROLE_KEYWORDS:
        for kw in keywords:
            if kw in text:
                return code
    return None


def has_intern_signal(title: str) -> bool:
    """True if the job title looks like a student/intern role."""
    return bool(_INTERN_PATTERNS.search(title))


def passes_location(location: str) -> bool:
    """
    True if job is in NYC area, remote, or location unknown.
    False if it's clearly another US/international city with no NYC mention.
    """
    if not location or location.strip() == "":
        return True   # unknown location — keep, can't tell

    loc = location.strip()

    # If NYC signal present anywhere → keep
    if _NYC_RE.search(loc):
        return True

    # If clearly another city with no NYC signal → exclude
    if _NON_NYC_RE.search(loc):
        return False

    # Ambiguous (e.g. just "United States" or generic) → keep
    return True


def passes_date_filter(job: dict) -> str:
    """
    Returns: 'include', 'maybe', or 'exclude'
    """
    parts = [
        job.get("title", ""),
        job.get("description", ""),
        job.get("start_date", ""),
        job.get("start_date_raw", ""),
    ]
    text = " ".join(p for p in parts if p).lower()

    # Hard excludes first
    for sig in EXCLUDE_SIGNALS:
        if sig in text:
            return "exclude"

    # Parsed ISO date
    raw = job.get("start_date_raw", "")
    if raw:
        try:
            d      = date.fromisoformat(raw[:10])
            cutoff = date.fromisoformat(START_AFTER)
            return "include" if d >= cutoff else "exclude"
        except ValueError:
            pass

    # Text signals
    for sig in START_DATE_SIGNALS:
        if sig in text:
            return "include"

    return "maybe"


def passes_filter(job: dict) -> bool:
    """
    Master filter. Mutates job to add 'role' and 'date_confidence'.
    Returns True to keep the job, False to discard.
    """

    title    = job.get("title", "").strip()
    desc     = job.get("description", "")
    location = job.get("location", "")

    # 1. Must have a title
    if not title:
        return False

    # 2. Must match a role keyword
    role = classify_role(title, desc)
    if not role:
        return False

    # 3. Title must contain an intern/student signal
    #    Exception: university source — research assistant postings often
    #    don't say "intern" explicitly
    source = job.get("source", "")
    if source != "University" and not has_intern_signal(title):
        return False

    # 4. Location must be NYC-area, remote, or unspecified
    if not passes_location(location):
        return False

    # 5. Date filter
    verdict = passes_date_filter(job)
    if verdict == "exclude":
        return False

    job["role"]            = role
    job["date_confidence"] = verdict
    return True
