import asyncio
import logging
import os
from contextlib import suppress

from aiohttp import web, ClientSession, ClientTimeout
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_settings
from database.db_setup import init_db
from handlers import get_routers
from utils.cache import AsyncCache
from utils.set_bot_commands import set_default_commands


# ---------------- LOGGING ----------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------- HEALTHCHECK SERVER ----------------
async def start_health_server() -> web.AppRunner:
    """
    Railway healthcheck:
    GET / -> 200 OK
    GET /ping -> 200 OK
    """
    port = int(os.getenv("PORT", "8080"))
    app = web.Application()

    async def root(_request):
        return web.Response(text="ok")

    async def ping(_request):
        return web.json_response({"status": "ok"})

    app.router.add_get("/", root)
    app.router.add_get("/ping", ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    logger.info("Healthcheck server started on 0.0.0.0:%s", port)
    return runner


# ---------------- MAIN ----------------
async def main():
    health_runner = None
    session = None

    try:
        # 1) START HEALTH SERVER FIRST (CRITICAL FOR RAILWAY)
        health_runner = await start_health_server()

        # 2) LOAD SETTINGS / DB
        settings = load_settings()
        await init_db()

        # 3) HTTP SESSION
        session = ClientSession(timeout=ClientTimeout(total=10))

        # 4) BOT + DISPATCHER
        bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode="HTML"),
        )
        dp = Dispatcher(storage=MemoryStorage())

        # 5) DEPENDENCIES
        dp["session"] = session
        dp["settings"] = settings
        dp["cache"] = AsyncCache(max_items=512)
        dp["semaphore"] = asyncio.Semaphore(10)
        dp["ui_state"] = {}
        dp["reply_menu_users"] = set()

        for router in get_routers():
            dp.include_router(router)

        await set_default_commands(bot)

        logger.info("Bot started polling")
        await dp.start_polling(bot)

    except Exception:
        logger.exception("Fatal error during startup")
        raise

    finally:
        if session:
            with suppress(Exception):
                await session.close()

        if health_runner:
            with suppress(Exception):
                await health_runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())