"""
utils/http.py
Shared async HTTP helpers with:
  - Exponential backoff retry (3 attempts)
  - Polite randomized delays between requests
  - User-agent rotation
  - Consistent timeout handling
"""

import asyncio
import random
import logging
import aiohttp

log = logging.getLogger(__name__)

_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
]

_TIMEOUT = aiohttp.ClientTimeout(total=25, connect=10)
_MAX_RETRIES = 3


def _headers() -> dict:
    return {
        "User-Agent": random.choice(_USER_AGENTS),
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }


async def _with_retry(coro_fn, retries: int = _MAX_RETRIES):
    """
    Call coro_fn() up to `retries` times with exponential backoff.
    coro_fn must be a zero-arg callable that returns a coroutine.
    Returns None on all failures.
    """
    for attempt in range(retries):
        try:
            return await coro_fn()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt < retries - 1:
                wait = (2 ** attempt) + random.uniform(0, 1)
                log.debug(f"Retry {attempt + 1}/{retries - 1} after {wait:.1f}s: {e}")
                await asyncio.sleep(wait)
            else:
                log.debug(f"All {retries} attempts failed: {e}")
                return None
        except Exception as e:
            log.debug(f"Non-retryable error: {e}")
            return None


async def get_json(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    delay: float = 0.5,
) -> dict | list | None:
    """GET JSON with polite delay and retry."""
    await asyncio.sleep(delay + random.uniform(0, 0.4))

    async def _do():
        async with session.get(url, params=params, headers=_headers(), timeout=_TIMEOUT) as resp:
            if resp.status == 200:
                return await resp.json(content_type=None)
            if resp.status in (404, 410):
                return None          # not retryable
            resp.raise_for_status()  # trigger retry on 5xx

    return await _with_retry(_do)


async def post_json(
    session: aiohttp.ClientSession,
    url: str,
    payload: dict,
    extra_headers: dict = None,
    delay: float = 1.0,
) -> dict | None:
    """POST JSON body, return JSON response."""
    await asyncio.sleep(delay + random.uniform(0, 0.4))
    headers = {**_headers(), "Content-Type": "application/json", **(extra_headers or {})}

    async def _do():
        async with session.post(url, json=payload, headers=headers, timeout=_TIMEOUT) as resp:
            if resp.status == 200:
                return await resp.json(content_type=None)
            if resp.status in (404, 410):
                return None
            resp.raise_for_status()

    return await _with_retry(_do)


async def get_html(
    session: aiohttp.ClientSession,
    url: str,
    delay: float = 1.2,
) -> str | None:
    """GET HTML text with polite delay and retry."""
    await asyncio.sleep(delay + random.uniform(0, 0.5))

    async def _do():
        async with session.get(url, headers=_headers(), timeout=_TIMEOUT) as resp:
            if resp.status == 200:
                return await resp.text(errors="replace")
            if resp.status in (404, 410, 403):
                return None
            resp.raise_for_status()

    return await _with_retry(_do)


def make_session() -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(limit=15, limit_per_host=3, ttl_dns_cache=300)
    return aiohttp.ClientSession(connector=connector, timeout=_TIMEOUT)
