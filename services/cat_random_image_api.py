import logging
from utils.http import request_json


logger = logging.getLogger(__name__)


async def fetch_random_cat_image(session, settings):
    headers = {}
    if settings.cat_api_key:
        headers["x-api-key"] = settings.cat_api_key
    data = await request_json(
        session,
        "GET",
        settings.cat_api_url,
        params=None,
        retries=3,
        backoff=0.5,
        headers=headers,
    )
    if not data or not isinstance(data, list):
        return None
    return data[0].get("url")
