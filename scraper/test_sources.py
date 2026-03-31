"""
test_sources.py
Run this locally to verify each scraper source works before deploying.

Usage:
  python test_sources.py              # test all sources
  python test_sources.py greenhouse   # test one source
  python test_sources.py greenhouse lever adzuna  # test multiple
"""

import asyncio
import json
import sys
import logging
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.WARNING)  # suppress source-level logs during test

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

SOURCES = {
    "adzuna":       scrape_adzuna,
    "usajobs":      scrape_usajobs,
    "remoteok":     scrape_remoteok,
    "greenhouse":   scrape_greenhouse,
    "lever":        scrape_lever,
    "universities": scrape_universities,
    "workday":      scrape_workday,
    "icims":        scrape_icims,
}

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


async def test_source(name: str, scraper_fn) -> dict:
    print(f"\n{BOLD}Testing {name}...{RESET}", flush=True)
    start = datetime.now()
    try:
        raw   = await scraper_fn()
        normd = [normalize_job(j) for j in raw]
        kept  = [j for j in normd if passes_filter(j)]
        elapsed = (datetime.now() - start).total_seconds()

        print(f"  {GREEN}✓ OK{RESET} — {len(raw)} raw → {len(kept)} passed filter ({elapsed:.1f}s)")

        if kept:
            sample = kept[0]
            print(f"  Sample: [{sample.get('role','?')}] {sample.get('title','')[:60]}")
            print(f"          {sample.get('company','')} · {sample.get('location','')} · {sample.get('start_date','')}")

        return {"name": name, "raw": len(raw), "kept": len(kept), "error": None, "elapsed": elapsed}

    except Exception as e:
        elapsed = (datetime.now() - start).total_seconds()
        print(f"  {RED}✗ FAILED{RESET} — {e} ({elapsed:.1f}s)")
        return {"name": name, "raw": 0, "kept": 0, "error": str(e), "elapsed": elapsed}


async def main():
    args = [a.lower() for a in sys.argv[1:]]

    if args:
        to_test = {k: v for k, v in SOURCES.items() if k in args}
        if not to_test:
            print(f"Unknown source(s): {args}")
            print(f"Available: {', '.join(SOURCES.keys())}")
            return
    else:
        to_test = SOURCES

    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}  Internship Scraper — Source Tests{RESET}")
    print(f"  Testing: {', '.join(to_test.keys())}")
    print(f"{BOLD}{'='*50}{RESET}")

    results = []
    for name, fn in to_test.items():
        r = await test_source(name, fn)
        results.append(r)

    # Summary
    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}  Summary{RESET}")
    print(f"{'─'*50}")
    total_raw  = sum(r["raw"]  for r in results)
    total_kept = sum(r["kept"] for r in results)

    for r in results:
        icon = f"{GREEN}✓{RESET}" if not r["error"] else f"{RED}✗{RESET}"
        warn = f"{YELLOW}(0 kept){RESET}" if r["kept"] == 0 and not r["error"] else ""
        print(f"  {icon} {r['name']:<14} {r['raw']:>4} raw → {r['kept']:>3} kept  {r['elapsed']:.1f}s {warn}")

    print(f"{'─'*50}")
    print(f"  Total:         {total_raw:>4} raw → {total_kept:>3} kept")
    print(f"{BOLD}{'='*50}{RESET}\n")

    if any(r["error"] for r in results):
        print(f"{YELLOW}Some sources failed. Check API keys in .env or environment.{RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
