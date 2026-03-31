"""
sources/remoteok.py
RemoteOK public API — completely free, no key needed.
Good for remote data/SWE internships.
"""

import logging
from datetime import date, datetime
from utils.http import get_json, make_session

log = logging.getLogger(__name__)

BASE_URL = "https://remoteok.com/api"

TAGS_OF_INTEREST = [
    "intern", "internship", "data", "engineer", "analyst",
    "scientist", "research", "ml", "ai", "backend",
]


def _parse_job(raw: dict) -> dict:
    ts = raw.get("date", "")
    try:
        posted = datetime.fromisoformat(ts).date().isoformat()
    except Exception:
        posted = date.today().isoformat()

    return {
        "title":          raw.get("position", ""),
        "company":        raw.get("company", "Unknown"),
        "location":       "Remote",
        "url":            raw.get("url", ""),
        "description":    raw.get("description", ""),
        "posted_date":    posted,
        "start_date_raw": "",
        "source":         "RemoteOK",
        "type":           "Remote",
    }


def _is_relevant(raw: dict) -> bool:
    tags  = [t.lower() for t in raw.get("tags", [])]
    title = raw.get("position", "").lower()
    return any(t in tags or t in title for t in TAGS_OF_INTEREST)


async def scrape_remoteok() -> list[dict]:
    async with make_session() as session:
        # RemoteOK requires a delay on first request
        data = await get_json(session, BASE_URL, delay=2.0)

    if not data or not isinstance(data, list):
        log.warning("RemoteOK: no data returned")
        return []

    # First item is a legal notice dict, skip it
    jobs = [_parse_job(raw) for raw in data[1:] if isinstance(raw, dict) and _is_relevant(raw)]
    log.info(f"RemoteOK: fetched {len(jobs)} relevant raw")
    return jobs
