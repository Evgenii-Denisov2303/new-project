import asyncio


async def acquire_or_notify(semaphore, call, timeout=0.1):
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        await call.answer("Бот сейчас занят, попробуй чуть позже.", show_alert=True)
        return False
