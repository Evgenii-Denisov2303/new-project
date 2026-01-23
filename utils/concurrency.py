import asyncio

from utils.i18n import t


async def acquire_or_notify(semaphore, call, lang: str = "ru", timeout=0.1):
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        await call.answer(t(lang, "facts.busy"), show_alert=True)
        return False
