"""
sources/universities.py
Scrapes university research / RA / REU opportunity pages.
Uses BeautifulSoup to parse HTML and extract job-like postings.
These pages vary wildly in structure, so we use heuristic extraction.
"""

import asyncio
import logging
import re
from datetime import date
from bs4 import BeautifulSoup
from utils.http import get_html, make_session
from config import UNIVERSITIES, ROLE_KEYWORDS

log = logging.getLogger(__name__)

# Anchor phrases that often precede a position title on university pages
POSITION_ANCHORS = re.compile(
    r"(research assistant|reu|undergraduate researcher|research intern|"
    r"data science intern|ml intern|software intern|lab assistant|"
    r"research fellow|summer fellow|fall position)",
    re.IGNORECASE,
)


def _extract_positions(html: str, university_name: str, source_url: str) -> list[dict]:
    """
    Heuristic extraction: look for headings, list items, or paragraphs
    that contain position-like text on university pages.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen_titles = set()

    # Strategy 1: Look for <a> tags whose text matches position keywords
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        if POSITION_ANCHORS.search(text) and len(text) > 10:
            href = a.get("href", "")
            if href and not href.startswith("http"):
                href = source_url.rstrip("/") + "/" + href.lstrip("/")
            if text not in seen_titles:
                seen_titles.add(text)
                results.append(_make_job(text, university_name, href or source_url))

    # Strategy 2: Look for headings (h2–h4) that contain position keywords
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if POSITION_ANCHORS.search(text) and len(text) > 10:
            if text not in seen_titles:
                seen_titles.add(text)
                # Try to find a sibling link
                sibling = tag.find_next_sibling("a") or tag.find("a")
                href = sibling.get("href", source_url) if sibling else source_url
                results.append(_make_job(text, university_name, href))

    # Strategy 3: List items
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if POSITION_ANCHORS.search(text) and 15 < len(text) < 200:
            if text not in seen_titles:
                seen_titles.add(text)
                a = li.find("a")
                href = a.get("href", source_url) if a else source_url
                results.append(_make_job(text, university_name, href))

    return results


def _make_job(title: str, university: str, url: str) -> dict:
    # Clean up title
    title = re.sub(r"\s+", " ", title).strip()
    # Guess type
    job_type = "Part-time" if "part" in title.lower() else None
    if "reu" in title.lower() or "fellowship" in title.lower():
        job_type = "Fellowship"

    return {
        "title":          title,
        "company":        university,
        "location":       "On Campus / Hybrid",
        "url":            url,
        "description":    "",
        "posted_date":    date.today().isoformat(),
        "start_date_raw": "",
        "source":         "University",
        "type":           job_type,
    }


async def _scrape_uni(session, uni: dict) -> list[dict]:
    results = []
    for url in uni["urls"]:
        html = await get_html(session, url, delay=1.5)
        if html:
            found = _extract_positions(html, uni["name"], url)
            results.extend(found)
            log.debug(f"  {uni['name']} @ {url}: {len(found)} positions")
    return results


async def scrape_universities() -> list[dict]:
    all_jobs = []
    async with make_session() as session:
        for i in range(0, len(UNIVERSITIES), 3):
            batch = UNIVERSITIES[i:i+3]
            results = await asyncio.gather(
                *[_scrape_uni(session, uni) for uni in batch],
                return_exceptions=True,
            )
            for uni, r in zip(batch, results):
                if isinstance(r, Exception):
                    log.debug(f"University {uni['name']} failed: {r}")
                else:
                    all_jobs.extend(r)
            await asyncio.sleep(2)

    log.info(f"Universities: found {len(all_jobs)} raw positions")
    return all_jobs
