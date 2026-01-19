import logging
from utils.http import request_json


logger = logging.getLogger(__name__)


async def fetch_random_cat_image(session, settings):
    data = await request_json(session, "GET", settings.cat_api_url)
    if not data or not isinstance(data, list):
        return None
    return data[0].get("url")
