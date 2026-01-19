import time
from database.db_setup import get_cache_value, set_cache_value


class TTLCache:
    def __init__(self, max_items=256):
        self.max_items = max_items
        self._data = {}

    def get(self, key):
        record = self._data.get(key)
        if not record:
            return None
        value, expires_at = record
        if expires_at and expires_at < time.time():
            self._data.pop(key, None)
            return None
        return value

    def set(self, key, value, ttl=None):
        if len(self._data) >= self.max_items:
            self._data.pop(next(iter(self._data)), None)
        expires_at = time.time() + ttl if ttl else None
        self._data[key] = (value, expires_at)


class AsyncCache:
    def __init__(self, max_items=512):
        self._memory = TTLCache(max_items=max_items)

    async def get(self, key):
        value = self._memory.get(key)
        if value is not None:
            return value

        value = await get_cache_value(key)
        if value is not None:
            self._memory.set(key, value, ttl=60)
        return value

    async def set(self, key, value, ttl=None):
        self._memory.set(key, value, ttl=ttl)
        await set_cache_value(key, value, ttl)
