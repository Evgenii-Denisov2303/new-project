import asyncio
import logging


logger = logging.getLogger(__name__)


async def request_json(session, method, url, params=None, retries=3, backoff=0.5):
    for attempt in range(retries):
        try:
            async with session.request(method, url, params=params) as response:
                if response.status == 429 and attempt < retries - 1:
                    retry_after = response.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else backoff * (2**attempt)
                    except ValueError:
                        delay = backoff * (2**attempt)
                    await asyncio.sleep(delay)
                    continue
                response.raise_for_status()
                return await response.json(content_type=None)
        except (asyncio.TimeoutError, Exception) as exc:
            if attempt >= retries - 1:
                logger.warning("HTTP request failed: %s %s (%s)", method, url, exc)
                return None
            await asyncio.sleep(backoff * (2**attempt))
    return None
