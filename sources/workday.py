"""
sources/workday.py
Workday CXS JSON search API.

URL strategy: Workday's externalPath is unreliable across tenants and
produces broken links. Instead we link directly to the company's
careers search page pre-filtered by the search term. This always works.
"""

import asyncio
import logging
from datetime import date
from utils.http import post_json, make_session
from config import WORKDAY_COMPANIES

log = logging.getLogger(__name__)

# Try these subdomain versions in order
_WD_VERSIONS = ["wd5", "wd1", "wd3", "wd12", "wd2"]

_SEARCH_TERMS = [
    "data engineer intern",
    "data analyst intern",
    "data science intern",
    "software engineer intern",
    "software engineer co-op",
    "data engineering co-op",
    "analytics intern",
    "machine learning intern",
    "business intelligence intern",
    "research intern",
]

_PAYLOAD_BASE = {"appliedFacets": {}, "limit": 20, "offset": 0}


def _cxs_url(tenant: str, version: str) -> str:
    return f"https://{tenant}.{version}.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs"


def _careers_url(tenant: str, version: str, search_term: str) -> str:
    """
    Human-facing careers search URL — always valid, always opens correctly.
    Pre-populated with the search term so the user lands on filtered results.
    """
    encoded = search_term.replace(" ", "%20")
    return (
        f"https://{tenant}.{version}.myworkdayjobs.com/en-US/External"
        f"?q={encoded}"
    )


def _parse_job(raw: dict, company_name: str, tenant: str, version: str, search_term: str) -> dict:
    # Use the general careers search URL — reliable across all tenants
    url = _careers_url(tenant, version, search_term)

    location = ", ".join(
        loc.get("descriptor", "")
        for loc in raw.get("jobPostingLocations", [])
        if loc.get("descriptor")
    )

    desc = ""
    jd = raw.get("jobDescription")
    if isinstance(jd, dict):
        desc = jd.get("descriptor", "")[:500]

    return {
        "title":          raw.get("title", ""),
        "company":        company_name,
        "location":       location,
        "url":            url,
        "description":    desc,
        "posted_date":    date.today().isoformat(),
        "start_date_raw": "",
        "source":         "Workday",
        "type":           None,
    }


async def _fetch_tenant(session, tenant: str, name: str) -> list[dict]:
    # Find a working version
    working_version = None
    for version in _WD_VERSIONS:
        url  = _cxs_url(tenant, version)
        data = await post_json(
            session, url,
            {**_PAYLOAD_BASE, "searchText": "intern"},
            delay=1.0,
        )
        if data is not None:
            working_version = version
            break

    if not working_version:
        log.debug(f"Workday/{tenant}: no working endpoint")
        return []

    jobs = []
    seen_titles = set()

    for term in _SEARCH_TERMS:
        url     = _cxs_url(tenant, working_version)
        payload = {**_PAYLOAD_BASE, "searchText": term}
        data    = await post_json(session, url, payload, delay=1.2)

        if not data or "jobPostings" not in data:
            continue

        for raw in data["jobPostings"]:
            title = raw.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                jobs.append(_parse_job(raw, name, tenant, working_version, term))

    return jobs


async def scrape_workday() -> list[dict]:
    all_jobs = []

    async with make_session() as session:
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
