import asyncio
import logging
import logging.handlers
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_settings
from database.db_setup import init_db
from handlers import get_routers
from utils.set_bot_commands import set_default_commands
from utils.cache import AsyncCache


async def main():
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s level=%(levelname)s name=%(name)s msg=%(message)s"
    )
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "bot.log"),
        maxBytes=1_000_000,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])

    settings = load_settings()
    await init_db()

    timeout = aiohttp.ClientTimeout(total=10)
    session = aiohttp.ClientSession(timeout=timeout)

    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    dp["session"] = session
    dp["settings"] = settings
    dp["cache"] = AsyncCache(max_items=512)
    dp["semaphore"] = asyncio.Semaphore(10)
    dp["ui_state"] = {}

    for router in get_routers():
        dp.include_router(router)

    await set_default_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
