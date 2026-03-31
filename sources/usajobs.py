"""
sources/usajobs.py
USAJobs API — completely free, great for federal research / national lab roles.
Sign up: https://developer.usajobs.gov/
Set env vars: USAJOBS_API_KEY, USAJOBS_EMAIL
"""

import os
import aiohttp
import logging
from datetime import date
from utils.http import make_session
from config import API_QUERIES

log = logging.getLogger(__name__)

BASE_URL = "https://data.usajobs.gov/api/search"

USAJOBS_QUERIES = [
    "data engineer intern",
    "data scientist intern",
    "data analyst intern",
    "research assistant",
    "software engineer intern",
    "machine learning intern",
    "computational research",
]


def _parse_job(raw: dict) -> dict:
    pos = raw.get("MatchedObjectDescriptor", {})
    return {
        "title":          pos.get("PositionTitle", ""),
        "company":        pos.get("OrganizationName", "US Federal Government"),
        "location":       ", ".join(
                            set(loc.get("LocationName", "") for loc in pos.get("PositionLocation", []))
                          ),
        "url":            pos.get("PositionURI", ""),
        "description":    pos.get("QualificationSummary", ""),
        "posted_date":    (pos.get("PublicationStartDate", "") or "")[:10] or date.today().isoformat(),
        "start_date_raw": (pos.get("PositionStartDate", "") or "")[:10],
        "source":         "USAJobs",
        "type":           "Internship" if "intern" in pos.get("PositionTitle", "").lower() else None,
    }


async def scrape_usajobs() -> list[dict]:
    api_key = os.getenv("USAJOBS_API_KEY")
    email   = os.getenv("USAJOBS_EMAIL")
    if not api_key or not email:
        log.warning("USAJobs: USAJOBS_API_KEY / USAJOBS_EMAIL not set, skipping")
        return []

    jobs = []
    headers = {
        "Host":            "data.usajobs.gov",
        "User-Agent":      email,
        "Authorization-Key": api_key,
    }

    async with make_session() as session:
        for query in USAJOBS_QUERIES:
            params = {
                "Keyword":          query,
                "ResultsPerPage":   50,
                "SortField":        "OpenDate",
                "SortDirection":    "Desc",
                "DatePosted":       7,  # last 7 days
            }
            try:
                async with session.get(BASE_URL, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                    if resp.status == 200:
                        data = await resp.json(content_type=None)
                        items = data.get("SearchResult", {}).get("SearchResultItems", [])
                        for raw in items:
                            jobs.append(_parse_job(raw))
            except Exception as e:
                log.warning(f"USAJobs query '{query}' failed: {e}")

    log.info(f"USAJobs: fetched {len(jobs)} raw")
    return jobs
