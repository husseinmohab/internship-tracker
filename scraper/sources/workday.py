"""
sources/workday.py
Workday career pages expose a semi-public CXS JSON search API.
We POST search queries directly — no headless browser needed for most tenants.
Falls back gracefully when a tenant slug doesn't match.
"""

import asyncio
import logging
from datetime import date
from utils.http import post_json, make_session
from config import WORKDAY_COMPANIES

log = logging.getLogger(__name__)

# Workday uses several subdomain patterns — we try the most common ones
_WD_URL_TEMPLATES = [
    "https://{tenant}.wd5.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
    "https://{tenant}.wd1.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
    "https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
]

_SEARCH_TERMS = [
    "data engineer intern",
    "data analyst intern",
    "data science intern",
    "software engineer intern co-op",
    "research intern fall 2026",
    "analytics intern",
    "machine learning intern",
]

_PAYLOAD_TEMPLATE = {
    "appliedFacets": {},
    "limit":         20,
    "offset":        0,
}


def _parse_job(raw: dict, company_name: str, base_url: str) -> dict:
    ext_path = raw.get("externalPath", "")
    # Build apply URL from the tenant's base domain
    domain   = "/".join(base_url.split("/")[:3])
    url      = domain + ext_path if ext_path else domain

    location = ", ".join(
        loc.get("descriptor", "")
        for loc in raw.get("jobPostingLocations", [])
        if loc.get("descriptor")
    )

    return {
        "title":          raw.get("title", ""),
        "company":        company_name,
        "location":       location,
        "url":            url,
        "description":    raw.get("jobDescription", {}).get("descriptor", "")[:500],
        "posted_date":    date.today().isoformat(),
        "start_date_raw": "",
        "source":         "Workday",
        "type":           None,
    }


async def _fetch_tenant(session, tenant: str, name: str) -> list[dict]:
    """Try each URL template until one works, then query all search terms."""
    working_url = None

    # Find a working URL template
    for template in _WD_URL_TEMPLATES:
        url  = template.format(tenant=tenant)
        data = await post_json(session, url, {**_PAYLOAD_TEMPLATE, "searchText": "intern"}, delay=1.0)
        if data is not None:
            working_url = url
            break

    if not working_url:
        log.debug(f"Workday/{tenant}: no working URL found")
        return []

    jobs = []
    for term in _SEARCH_TERMS:
        payload = {**_PAYLOAD_TEMPLATE, "searchText": term}
        data    = await post_json(session, working_url, payload, delay=1.2)
        if data and "jobPostings" in data:
            for raw in data["jobPostings"]:
                jobs.append(_parse_job(raw, name, working_url))

    return jobs


async def scrape_workday() -> list[dict]:
    all_jobs = []

    async with make_session() as session:
        # Run in small batches — Workday is rate-sensitive
        for i in range(0, len(WORKDAY_COMPANIES), 3):
            batch   = WORKDAY_COMPANIES[i:i+3]
            results = await asyncio.gather(
                *[_fetch_tenant(session, tenant, name) for tenant, name in batch],
                return_exceptions=True,
            )
            for (tenant, name), r in zip(batch, results):
                if isinstance(r, Exception):
                    log.debug(f"Workday/{tenant} error: {r}")
                elif r:
                    log.debug(f"Workday/{tenant}: {len(r)} jobs")
                    all_jobs.extend(r)
            await asyncio.sleep(2.5)

    log.info(f"Workday: {len(all_jobs)} raw across {len(WORKDAY_COMPANIES)} companies")
    return all_jobs
