"""
sources/workday.py
Workday career pages expose a semi-public CXS JSON search API.
We POST search queries directly — no headless browser needed for most tenants.

URL fix: Workday job posting URLs follow the pattern:
  https://{tenant}.wd5.myworkdayjobs.com/en-US/External/{externalPath}
NOT the CXS API path.
"""

import asyncio
import logging
from datetime import date
from utils.http import post_json, make_session
from config import WORKDAY_COMPANIES

log = logging.getLogger(__name__)

_WD_URL_TEMPLATES = [
    "https://{tenant}.wd5.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
    "https://{tenant}.wd1.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
    "https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant}/External/jobs",
]

# The apply URL base — different from the CXS API base
_WD_APPLY_TEMPLATES = [
    "https://{tenant}.wd5.myworkdayjobs.com/en-US/External",
    "https://{tenant}.wd1.myworkdayjobs.com/en-US/External",
    "https://{tenant}.wd3.myworkdayjobs.com/en-US/External",
]

_SEARCH_TERMS = [
    "data engineer intern",
    "data analyst intern",
    "data science intern",
    "software engineer intern",
    "software engineer co-op",
    "research intern fall",
    "analytics intern",
    "machine learning intern",
    "business intelligence intern",
    "data engineering co-op",
]

_PAYLOAD_TEMPLATE = {
    "appliedFacets": {},
    "limit":         20,
    "offset":        0,
}


def _build_apply_url(tenant: str, wd_version: str, ext_path: str) -> str:
    """
    Construct the correct human-facing apply URL.
    ext_path from API looks like: /job/New-York/Data-Engineer-Intern_R-12345
    Apply URL: https://{tenant}.wd{N}.myworkdayjobs.com/en-US/External/job/...
    """
    base = f"https://{tenant}.{wd_version}.myworkdayjobs.com/en-US/External"
    if ext_path:
        # ext_path already starts with /job/...
        return base + ext_path
    return base


def _parse_job(raw: dict, company_name: str, tenant: str, wd_version: str) -> dict:
    ext_path = raw.get("externalPath", "")
    url      = _build_apply_url(tenant, wd_version, ext_path)

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
        "description":    raw.get("jobDescription", {}).get("descriptor", "")[:500]
                          if isinstance(raw.get("jobDescription"), dict) else "",
        "posted_date":    date.today().isoformat(),
        "start_date_raw": "",
        "source":         "Workday",
        "type":           None,
    }


async def _fetch_tenant(session, tenant: str, name: str) -> list[dict]:
    """Try each Workday subdomain version until one responds."""
    working_url = None
    wd_version  = None

    for i, template in enumerate(_WD_URL_TEMPLATES):
        url  = template.format(tenant=tenant)
        data = await post_json(
            session, url,
            {**_PAYLOAD_TEMPLATE, "searchText": "intern"},
            delay=1.0,
        )
        if data is not None:
            working_url = url
            wd_version  = ["wd5", "wd1", "wd3"][i]
            break

    if not working_url:
        log.debug(f"Workday/{tenant}: no working endpoint found")
        return []

    jobs = []
    for term in _SEARCH_TERMS:
        payload = {**_PAYLOAD_TEMPLATE, "searchText": term}
        data    = await post_json(session, working_url, payload, delay=1.2)
        if data and "jobPostings" in data:
            for raw in data["jobPostings"]:
                jobs.append(_parse_job(raw, name, tenant, wd_version))

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
