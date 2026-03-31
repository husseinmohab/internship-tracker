"""
sources/lever.py
Lever also has a public JSON API.
Endpoint: https://api.lever.co/v0/postings/{slug}?mode=json
"""

import asyncio
import logging
from datetime import date, datetime
from utils.http import get_json, make_session
from config import LEVER_COMPANIES

log = logging.getLogger(__name__)

BASE = "https://api.lever.co/v0/postings/{slug}?mode=json"


def _parse_job(raw: dict, company_name: str) -> dict:
    # Lever timestamp is Unix ms
    ts = raw.get("createdAt", 0)
    try:
        posted = datetime.utcfromtimestamp(ts / 1000).date().isoformat()
    except Exception:
        posted = date.today().isoformat()

    # Combine text fields for description
    lists = raw.get("lists", [])
    desc_parts = [raw.get("descriptionPlain", "")]
    for lst in lists:
        desc_parts.append(lst.get("text", ""))
        desc_parts.append(" ".join(lst.get("content", [])))
    desc = " ".join(desc_parts)[:2000]

    # Location
    categories = raw.get("categories", {})
    location   = categories.get("location", "") or raw.get("workplaceType", "")

    return {
        "title":          raw.get("text", ""),
        "company":        company_name,
        "location":       location,
        "url":            raw.get("hostedUrl", ""),
        "description":    desc,
        "posted_date":    posted,
        "start_date_raw": "",
        "source":         "Lever",
        "type":           None,
    }


async def _fetch_company(session, slug: str, name: str) -> list[dict]:
    url  = BASE.format(slug=slug)
    data = await get_json(session, url, delay=0.5)
    if not data or not isinstance(data, list):
        return []
    return [_parse_job(j, name) for j in data]


async def scrape_lever() -> list[dict]:
    all_jobs = []
    async with make_session() as session:
        for i in range(0, len(LEVER_COMPANIES), 5):
            batch = LEVER_COMPANIES[i:i+5]
            results = await asyncio.gather(
                *[_fetch_company(session, slug, name) for slug, name in batch],
                return_exceptions=True,
            )
            for (slug, name), r in zip(batch, results):
                if isinstance(r, Exception):
                    log.debug(f"Lever/{slug} failed: {r}")
                else:
                    all_jobs.extend(r)
            await asyncio.sleep(1)

    log.info(f"Lever: fetched {len(all_jobs)} raw across {len(LEVER_COMPANIES)} companies")
    return all_jobs
