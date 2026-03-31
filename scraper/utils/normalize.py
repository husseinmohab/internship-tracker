"""
utils/normalize.py
Cleans up raw job fields before they're written to jobs.json:
  - Strips HTML artifacts from titles
  - Standardizes location strings
  - Detects job type (Co-op, Part-time, Remote) from title/description
  - Extracts start date hints from free text
"""

import re
from datetime import date


# ── Title cleanup ──────────────────────────────────────────────────────────────

_HTML_TAG   = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")
_PARENS     = re.compile(r"\([^)]{0,60}\)")   # remove short parenthetical notes

def clean_title(title: str) -> str:
    title = _HTML_TAG.sub(" ", title)
    title = _PARENS.sub("", title)
    title = _WHITESPACE.sub(" ", title).strip()
    # Title-case if all caps, leave mixed-case alone
    if title == title.upper() and len(title) > 3:
        title = title.title()
    return title


# ── Location normalization ─────────────────────────────────────────────────────

_REMOTE_RE   = re.compile(r"\bremote\b", re.IGNORECASE)
_NYC_ALIASES = re.compile(
    r"\b(new york(,\s*ny)?|nyc|manhattan|brooklyn|queens|bronx|new york city)\b",
    re.IGNORECASE,
)
_NJ_RE = re.compile(r"\b(new jersey|nj|hoboken|jersey city|princeton|newark)\b", re.IGNORECASE)

def normalize_location(loc: str) -> str:
    if not loc:
        return ""
    loc = _WHITESPACE.sub(" ", loc.strip())
    if _REMOTE_RE.search(loc):
        return "Remote"
    if _NYC_ALIASES.search(loc):
        return "New York, NY"
    if _NJ_RE.search(loc):
        # Keep original NJ city but append state
        match = _NJ_RE.search(loc)
        city  = match.group(0).strip().title()
        return f"{city}, NJ"
    # Truncate very long location strings
    if len(loc) > 60:
        loc = loc[:57] + "…"
    return loc


# ── Job type detection ─────────────────────────────────────────────────────────

def detect_type(title: str, description: str) -> str | None:
    text = (title + " " + description).lower()
    if re.search(r"\bco-?op\b", text):
        return "Co-op"
    if re.search(r"\bpart.?time\b", text):
        return "Part-time"
    if re.search(r"\bfull.?time\b", text):
        return "Full-time"
    if _REMOTE_RE.search(title):
        return "Remote"
    if re.search(r"\breu\b|\bfellowship\b", text):
        return "Fellowship"
    return None


# ── Start date extraction ──────────────────────────────────────────────────────

_START_DATE_PATTERNS = [
    # "August 2026", "Sep 2026", "September 2026"
    (re.compile(r"\b(august|september|october|november|aug|sep|sept|oct|nov)\s+2026\b", re.IGNORECASE), lambda m: m.group(0).title()),
    # "Fall 2026"
    (re.compile(r"\bfall\s+2026\b", re.IGNORECASE), lambda m: "Fall 2026"),
    # "Fall '26"
    (re.compile(r"\bfall\s+'?26\b", re.IGNORECASE), lambda m: "Fall 2026"),
    # "2026-08", "2026-09" style
    (re.compile(r"\b2026-(0[89]|1[012])\b"), lambda m: f"Month {m.group(1)} 2026"),
]

def extract_start_date(title: str, description: str) -> str:
    text = title + " " + description
    for pattern, formatter in _START_DATE_PATTERNS:
        m = pattern.search(text)
        if m:
            return formatter(m)
    return ""


# ── Master normalizer ──────────────────────────────────────────────────────────

def normalize_job(job: dict) -> dict:
    """
    Normalize a raw job dict in place. Returns the same dict.
    Always call this before passing to the filter.
    """
    job["title"]    = clean_title(job.get("title", ""))
    job["location"] = normalize_location(job.get("location", ""))
    job["company"]  = job.get("company", "").strip()

    # Detect type if not already set
    if not job.get("type"):
        job["type"] = detect_type(job.get("title", ""), job.get("description", ""))

    # Extract start date hint if not already parsed
    if not job.get("start_date"):
        job["start_date"] = extract_start_date(
            job.get("title", ""), job.get("description", "")
        )

    # Keep description short — used only for keyword matching, not displayed
    desc = job.get("description", "")
    job["description"] = desc[:500] if desc else ""

    # Ensure posted_date is set
    if not job.get("posted_date"):
        job["posted_date"] = date.today().isoformat()

    return job
