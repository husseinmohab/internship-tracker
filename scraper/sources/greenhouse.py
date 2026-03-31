"""
sources/greenhouse.py
Greenhouse has a public JSON API for every company's board.
No auth needed — this is intentionally public.
Endpoint: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
"""

import asyncio
import logging
from datetime import date, datetime
from utils.http import get_json, make_session
from config import GREENHOUSE_COMPANIES

log = logging.getLogger(__name__)

BASE = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"


def _parse_job(raw: dict, company_name: str) -> dict:
    # Extract location
    loc = raw.get("location", {})
    location = loc.get("name", "") if isinstance(loc, dict) else str(loc)

    # Parse date
    ts = raw.get("updated_at", "") or raw.get("created_at", "")
    try:
        posted = datetime.fromisoformat(ts.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        posted = date.today().isoformat()

    # Greenhouse gives us full HTML description via ?content=true
    desc_html = raw.get("content", "") or ""
    # Strip basic HTML tags for keyword matching
    import re
    desc_text = re.sub(r"<[^>]+>", " ", desc_html)

    return {
        "title":          raw.get("title", ""),
        "company":        company_name,
        "location":       location,
        "url":            raw.get("absolute_url", ""),
        "description":    desc_text[:2000],
        "posted_date":    posted,
        "start_date_raw": "",
        "source":         "Greenhouse",
        "type":           None,
    }


async def _fetch_company(session, slug: str, name: str) -> list[dict]:
    url  = BASE.format(slug=slug)
    data = await get_json(session, url, params={"content": "true"}, delay=0.5)
    if not data:
        return []
    return [_parse_job(j, name) for j in data.get("jobs", [])]


async def scrape_greenhouse() -> list[dict]:
    all_jobs = []
    async with make_session() as session:
        # Batch in groups of 5 to be polite
        for i in range(0, len(GREENHOUSE_COMPANIES), 5):
            batch = GREENHOUSE_COMPANIES[i:i+5]
            results = await asyncio.gather(
                *[_fetch_company(session, slug, name) for slug, name in batch],
                return_exceptions=True,
            )
            for (slug, name), r in zip(batch, results):
                if isinstance(r, Exception):
                    log.debug(f"Greenhouse/{slug} failed: {r}")
                else:
                    all_jobs.extend(r)
            await asyncio.sleep(1)

    log.info(f"Greenhouse: fetched {len(all_jobs)} raw across {len(GREENHOUSE_COMPANIES)} companies")
    return all_jobs
