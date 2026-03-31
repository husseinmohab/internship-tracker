"""
utils/dedup.py
Deduplicates jobs across runs using a stable hash of (title, company, url).
Existing jobs are preserved; new ones are added; no duplicates.
"""

import hashlib


def make_id(job: dict) -> str:
    """Stable ID from title + company + url."""
    key = f"{job.get('title','').lower().strip()}|{job.get('company','').lower().strip()}|{job.get('url','').strip()}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def dedup_jobs(existing: list[dict], new_jobs: list[dict]) -> list[dict]:
    """
    Merge existing + new, deduplicating by stable ID.
    New jobs take precedence (fresher data), but we keep existing
    jobs that no longer appear (they may still be open).
    """
    seen = {}

    # Index existing by id
    for job in existing:
        jid = job.get("id") or make_id(job)
        job["id"] = jid
        seen[jid] = job

    # Add/overwrite with new jobs
    for job in new_jobs:
        jid = make_id(job)
        job["id"] = jid
        if jid not in seen:
            seen[jid] = job
        else:
            # Update URL and posted_date but keep user-set status
            seen[jid].update({k: v for k, v in job.items() if k != "id"})

    return list(seen.values())
