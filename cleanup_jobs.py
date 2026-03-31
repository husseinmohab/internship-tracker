"""
cleanup_jobs.py
One-time script to purge bad jobs (senior, wrong location, etc.)
from the existing docs/jobs.json using the current filter logic.

Run once after deploying filter fixes:
  python cleanup_jobs.py

Rewrites docs/jobs.json in place with only clean jobs.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# Make sure we can import from utils/
sys.path.insert(0, str(Path(__file__).parent))

from utils.filter import passes_filter

JOBS_PATH = Path("docs/jobs.json")

def main():
    if not JOBS_PATH.exists():
        print("docs/jobs.json not found — nothing to clean.")
        return

    data     = json.loads(JOBS_PATH.read_text())
    before   = data.get("jobs", [])
    print(f"Before: {len(before)} jobs")

    # Re-run filter on every existing job
    # passes_filter mutates the job dict, so work on copies
    kept = []
    removed = []
    for job in before:
        j = dict(job)  # shallow copy
        if passes_filter(j):
            kept.append(job)   # keep original (with existing status etc.)
        else:
            removed.append(job.get("title", "?") + " @ " + job.get("company", "?"))

    print(f"After:  {len(kept)} jobs ({len(removed)} removed)")

    if removed:
        print("\nRemoved:")
        for r in removed[:30]:
            print(f"  - {r}")
        if len(removed) > 30:
            print(f"  ... and {len(removed) - 30} more")

    # Write cleaned file
    data["jobs"]         = sorted(kept, key=lambda j: j["posted_date"], reverse=True)
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    JOBS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(kept)} clean jobs → {JOBS_PATH}")

if __name__ == "__main__":
    main()
