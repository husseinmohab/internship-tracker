"""
Fall 2026 Internship Scraper
Runs daily via GitHub Actions. Writes results to docs/jobs.json
and a run log to docs/run_log.json for dashboard diagnostics.

Sources:
  Layer 1 — APIs      : Adzuna, USAJobs, RemoteOK
  Layer 2 — ATS       : Greenhouse, Lever (public JSON endpoints)
  Layer 3 — Unis      : Ivy League + NYC-area research/RA/REU pages
  Layer 4 — Workday   : Workday CXS API (big enterprises)
  Layer 4b— iCIMS     : Banks, Big 4, consulting firms
"""

import asyncio
import json
import logging
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# Load .env if present (local dev only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from sources.adzuna       import scrape_adzuna
from sources.usajobs      import scrape_usajobs
from sources.remoteok     import scrape_remoteok
from sources.greenhouse   import scrape_greenhouse
from sources.lever        import scrape_lever
from sources.universities import scrape_universities
from sources.workday      import scrape_workday
from sources.icims        import scrape_icims
from utils.normalize      import normalize_job
from utils.filter         import passes_filter
from utils.dedup          import dedup_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

OUTPUT_PATH = Path("docs/jobs.json")
LOG_PATH    = Path("docs/run_log.json")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


async def run_source(name: str, coro) -> tuple:
    """Run a scraper coroutine and return (name, jobs, error_or_None)."""
    try:
        jobs = await coro
        return name, jobs, None
    except Exception as e:
        log.warning(f"{name} failed: {e}")
        return name, [], str(e)


async def main():
    log.info("=" * 55)
    log.info("  Fall 2026 Internship Scraper")
    log.info(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    log.info("=" * 55)

    run_log = {"started_at": datetime.now(timezone.utc).isoformat(), "sources": {}}

    # ── Run all sources concurrently ───────────────────────────────────
    sources = [
        ("Adzuna",       scrape_adzuna()),
        ("USAJobs",      scrape_usajobs()),
        ("RemoteOK",     scrape_remoteok()),
        ("Greenhouse",   scrape_greenhouse()),
        ("Lever",        scrape_lever()),
        ("iCIMS",        scrape_icims()),
        ("Universities", scrape_universities()),
        ("Workday",      scrape_workday()),
    ]

    all_raw = []
    results = await asyncio.gather(*[run_source(n, c) for n, c in sources])

    for name, jobs, error in results:
        run_log["sources"][name] = {
            "raw_count": len(jobs),
            "error":     error,
            "status":    "ok" if not error else "error",
        }
        all_raw.extend(jobs)
        status = "✓" if not error else "✗"
        log.info(f"  {status} {name}: {len(jobs)} raw {'  — ' + error if error else ''}")

    log.info(f"\nTotal raw: {len(all_raw)}")

    # ── Normalize ──────────────────────────────────────────────────────
    normalized = [normalize_job(j) for j in all_raw]

    # ── Filter ─────────────────────────────────────────────────────────
    filtered = [j for j in normalized if passes_filter(j)]
    log.info(f"After filter: {len(filtered)}")
    run_log["filtered_count"] = len(filtered)

    # ── Deduplicate + merge with existing ──────────────────────────────
    existing = []
    if OUTPUT_PATH.exists():
        try:
            data     = json.loads(OUTPUT_PATH.read_text())
            existing = data.get("jobs", [])
        except Exception:
            pass

    merged = dedup_jobs(existing, filtered)

    # Strip large/internal fields before saving
    for j in merged:
        j.pop("description",    None)
        j.pop("start_date_raw", None)

    log.info(f"After dedup + merge: {len(merged)}")
    run_log["total_jobs"] = len(merged)

    # ── Write docs/jobs.json ───────────────────────────────────────────
    now    = datetime.now(timezone.utc).isoformat()
    output = {
        "last_updated": now,
        "jobs": sorted(merged, key=lambda j: j["posted_date"], reverse=True),
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    log.info(f"Wrote {len(merged)} jobs → {OUTPUT_PATH}")

    # ── Write docs/run_log.json ────────────────────────────────────────
    run_log["finished_at"] = now
    run_log["success"]     = True
    LOG_PATH.write_text(json.dumps(run_log, indent=2))
    log.info(f"Run log → {LOG_PATH}")

    log.info("=" * 55)
    log.info("  Done ✓")
    log.info("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
