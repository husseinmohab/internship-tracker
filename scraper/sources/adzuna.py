"""
sources/adzuna.py
Adzuna Jobs API — free tier, solid aggregator coverage.
Sign up: https://developer.adzuna.com/
Set env vars: ADZUNA_APP_ID, ADZUNA_APP_KEY
"""

import os
import aiohttp
import logging
from datetime import date
from utils.http import get_json, make_session
from config import API_QUERIES

log = logging.getLogger(__name__)

BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"


def _parse_job(raw: dict) -> dict:
    return {
        "title":          raw.get("title", ""),
        "company":        raw.get("company", {}).get("display_name", "Unknown"),
        "location":       raw.get("location", {}).get("display_name", ""),
        "url":            raw.get("redirect_url", ""),
        "description":    raw.get("description", ""),
        "posted_date":    (raw.get("created", "") or "")[:10] or date.today().isoformat(),
        "start_date_raw": "",
        "source":         "Adzuna",
        "type":           None,
    }


async def scrape_adzuna() -> list[dict]:
    app_id  = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        log.warning("Adzuna: ADZUNA_APP_ID / ADZUNA_APP_KEY not set, skipping")
        return []

    jobs = []
    async with make_session() as session:
        for query in API_QUERIES:
            params = {
                "app_id":         app_id,
                "app_key":        app_key,
                "what":           query,
                "where":          "New York",
                "distance":       50,
                "results_per_page": 50,
                "sort_by":        "date",
                "content-type":   "application/json",
            }
            data = await get_json(session, BASE_URL, params=params, delay=0.8)
            if data and "results" in data:
                for raw in data["results"]:
                    jobs.append(_parse_job(raw))

    log.info(f"Adzuna: fetched {len(jobs)} raw")
    return jobs
