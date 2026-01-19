import logging
from utils.http import request_json


logger = logging.getLogger(__name__)


async def translate_text(session, settings, cache, text, target_language="ru"):
    if not text:
        return None

    cache_key = f"translate:{target_language}:{text}"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    params = {
        "client": "gtx",
        "sl": "en",
        "tl": target_language,
        "dt": "t",
        "q": text,
    }

    result = await request_json(
        session,
        "GET",
        settings.translate_api_url,
        params=params,
        retries=4,
        backoff=0.6,
    )
    if not result:
        return None

    translated = result[0][0][0] if result else None
    if translated:
        await cache.set(cache_key, translated, ttl=600)
    return translated
