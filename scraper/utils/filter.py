"""
utils/filter.py
Decides whether a normalized job dict is relevant:
  - Role must match one of our 6 categories
  - Start date must be after Aug 6 2026, or ambiguous (no date info)
  - No explicit summer-only signals

NOTE: This runs AFTER normalize_job(), so field names are already clean.
  - job["start_date"]     → human string like "Fall 2026" or ""
  - job["start_date_raw"] → ISO date string or "" (set by some sources)
  - job["description"]    → plain text, already truncated
"""

import re
from datetime import date
from config import ROLE_KEYWORDS, START_DATE_SIGNALS, EXCLUDE_SIGNALS, START_AFTER


def classify_role(title: str, description: str = "") -> str | None:
    """Return role code (de/da/ds/swe/re/ra) or None if no match."""
    text = (title + " " + description).lower()
    for code, keywords in ROLE_KEYWORDS:
        for kw in keywords:
            if kw in text:
                return code
    return None


def passes_date_filter(job: dict) -> str:
    """
    Returns one of: 'include', 'maybe', 'exclude'
      'include' → clear fall 2026 / post-Aug-6 signal
      'maybe'   → no date info at all; keep but flag
      'exclude' → explicitly summer 2026 or before cutoff
    """
    # Build one big text blob from all date-relevant fields
    parts = [
        job.get("title", ""),
        job.get("description", ""),
        job.get("start_date", ""),       # set by normalize_job
        job.get("start_date_raw", ""),   # set by some API sources
    ]
    text = " ".join(p for p in parts if p).lower()

    # ── Hard excludes first ────────────────────────────────────────────
    for sig in EXCLUDE_SIGNALS:
        if sig in text:
            return "exclude"

    # ── Parsed ISO date check ─────────────────────────────────────────
    raw = job.get("start_date_raw", "")
    if raw:
        try:
            d      = date.fromisoformat(raw[:10])
            cutoff = date.fromisoformat(START_AFTER)
            return "include" if d >= cutoff else "exclude"
        except ValueError:
            pass

    # ── Text signal check ─────────────────────────────────────────────
    for sig in START_DATE_SIGNALS:
        if sig in text:
            return "include"

    # ── No date info at all → keep with low confidence ────────────────
    return "maybe"


def passes_filter(job: dict) -> bool:
    """Master filter. Mutates job to add 'role' and 'date_confidence'. Returns True to keep."""

    # ── Must have a non-empty title ───────────────────────────────────
    if not job.get("title", "").strip():
        return False

    # ── Must match a role ─────────────────────────────────────────────
    role = classify_role(job.get("title", ""), job.get("description", ""))
    if not role:
        return False
    job["role"] = role

    # ── Date filter ───────────────────────────────────────────────────
    verdict = passes_date_filter(job)
    if verdict == "exclude":
        return False

    job["date_confidence"] = verdict   # 'include' | 'maybe'
    return True
