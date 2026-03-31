"""
sources/icims.py
iCIMS is the ATS used by many banks, consulting firms, and large enterprises.
Unlike Greenhouse/Lever, iCIMS doesn't have a unified public API —
each company has its own subdomain. We use their search endpoint pattern.

Companies: SMBC, Deloitte, PwC, EY, KPMG, Accenture, Booz Allen,
           McKinsey (some roles), Verizon, AT&T, etc.
"""

import asyncio
import logging
import re
from datetime import date
from bs4 import BeautifulSoup
from utils.http import get_html, get_json, make_session

log = logging.getLogger(__name__)

# iCIMS company configs
# Format: (base_url, company_name, customer_id_or_path)
# The search URL pattern varies slightly per company.
ICIMS_COMPANIES = [
    # Finance
    {
        "name":    "SMBC",
        "search":  "https://careers.smbc-group.com/search/?q={query}&locationsearch=new+york",
        "listing": "https://careers.smbc-group.com",
    },
    {
        "name":    "Citi",
        "search":  "https://jobs.citi.com/search-jobs/{query}/185/1",
        "listing": "https://jobs.citi.com",
    },
    # Consulting / Big 4
    {
        "name":    "Deloitte",
        "search":  "https://apply.deloitte.com/careers/SearchJobs/{query}?listFilterMode=1&jobRecordsPerPage=20",
        "listing": "https://apply.deloitte.com",
    },
    {
        "name":    "EY",
        "search":  "https://careers.ey.com/ey/search/?q={query}&locationsearch=new+york",
        "listing": "https://careers.ey.com",
    },
    {
        "name":    "KPMG",
        "search":  "https://jobs.kpmg.us/search-jobs/{query}",
        "listing": "https://jobs.kpmg.us",
    },
    # Tech / Consulting
    {
        "name":    "Accenture",
        "search":  "https://www.accenture.com/us-en/careers/jobsearch?jk={query}&sb=1&vw=0&is_rj=0",
        "listing": "https://www.accenture.com",
    },
    {
        "name":    "Booz Allen Hamilton",
        "search":  "https://careers.boozallen.com/jobs/search?q={query}&location=new+york",
        "listing": "https://careers.boozallen.com",
    },
    # Healthcare / Pharma
    {
        "name":    "UnitedHealth Group",
        "search":  "https://careers.unitedhealthgroup.com/search-jobs/{query}",
        "listing": "https://careers.unitedhealthgroup.com",
    },
    # Retail / Logistics
    {
        "name":    "FedEx",
        "search":  "https://careers.fedex.com/fedex/search-jobs/{query}",
        "listing": "https://careers.fedex.com",
    },
]

SEARCH_TERMS = [
    "data engineer intern",
    "data analyst intern",
    "data science intern",
    "software engineer intern co-op",
    "research intern fall 2026",
]


def _extract_jobs_from_html(html: str, company_name: str, base_url: str) -> list[dict]:
    """
    Generic HTML extractor for iCIMS-style career pages.
    Looks for job listing patterns common to iCIMS markup.
    """
    soup  = BeautifulSoup(html, "html.parser")
    jobs  = []

    # iCIMS typically uses article tags or divs with class containing 'job'
    selectors = [
        soup.find_all("article"),
        soup.find_all("div", class_=re.compile(r"job|listing|result|position", re.I)),
        soup.find_all("li",  class_=re.compile(r"job|listing|result|position", re.I)),
    ]

    seen = set()
    for elements in selectors:
        for el in elements:
            # Extract title
            title_el = (
                el.find(["h2", "h3", "h4"]) or
                el.find(class_=re.compile(r"title|position|job.?name", re.I))
            )
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not title or title in seen or len(title) < 5:
                continue
            seen.add(title)

            # Extract URL
            link = el.find("a", href=True)
            url  = ""
            if link:
                href = link["href"]
                url  = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")

            # Extract location
            loc_el = el.find(class_=re.compile(r"location|city|loc", re.I))
            loc    = loc_el.get_text(strip=True) if loc_el else ""

            jobs.append({
                "title":          title,
                "company":        company_name,
                "location":       loc,
                "url":            url or base_url,
                "description":    el.get_text(strip=True)[:300],
                "posted_date":    date.today().isoformat(),
                "start_date_raw": "",
                "source":         "iCIMS",
                "type":           None,
            })

    return jobs


async def _scrape_company(session, company: dict) -> list[dict]:
    all_jobs = []
    for term in SEARCH_TERMS:
        url  = company["search"].format(query=term.replace(" ", "+"))
        html = await get_html(session, url, delay=1.5)
        if html:
            jobs = _extract_jobs_from_html(html, company["name"], company["listing"])
            all_jobs.extend(jobs)
    return all_jobs


async def scrape_icims() -> list[dict]:
    all_jobs = []
    async with make_session() as session:
        for i in range(0, len(ICIMS_COMPANIES), 2):
            batch   = ICIMS_COMPANIES[i:i+2]
            results = await asyncio.gather(
                *[_scrape_company(session, c) for c in batch],
                return_exceptions=True,
            )
            for company, r in zip(batch, results):
                if isinstance(r, Exception):
                    log.debug(f"iCIMS/{company['name']} failed: {r}")
                else:
                    log.debug(f"iCIMS/{company['name']}: {len(r)} raw")
                    all_jobs.extend(r)
            await asyncio.sleep(2)

    log.info(f"iCIMS: found {len(all_jobs)} raw across {len(ICIMS_COMPANIES)} companies")
    return all_jobs
