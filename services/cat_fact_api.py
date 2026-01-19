import logging
from utils.http import request_json


logger = logging.getLogger(__name__)


async def fetch_cat_fact(session, settings, cache):
    cache_key = "cat_fact"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    data = await request_json(session, "GET", settings.cat_facts_api_url)
    if not data:
        return None
    fact = data.get("fact")
    if fact:
        await cache.set(cache_key, fact, ttl=5)
    return fact
