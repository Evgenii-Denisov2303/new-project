import asyncio
import logging
import os
from contextlib import suppress

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_settings
from database.db_setup import init_db
from handlers import get_routers
from utils.cache import AsyncCache
from utils.set_bot_commands import set_default_commands


def _setup_logging() -> None:
    # Railway лучше всего читает stdout/stderr
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s level=%(levelname)s name=%(name)s msg=%(message)s",
    )


async def _start_healthcheck_server() -> web.AppRunner:
    """
    Railway healthcheck: GET / должен отвечать 200.
    Важно: слушаем 0.0.0.0 и порт из переменной PORT.
    """
    port = int(os.getenv("PORT", "8080"))

    app = web.Application()

    async def root(_request: web.Request) -> web.Response:
        return web.Response(text="ok")

    async def ping(_request: web.Request) -> web.Response:
        return web.json_response({"status": "ok"})

    app.router.add_get("/", root)
    app.router.add_get("/ping", ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    logging.getLogger(__name__).info("Healthcheck server listening on 0.0.0.0:%s", port)
    return runner


async def main() -> None:
    _setup_logging()
    log = logging.getLogger(__name__)

    # 1) СНАЧАЛА healthcheck, чтобы Railway не валил деплой
    health_runner: web.AppRunner | None = None
    try:
        health_runner = await _start_healthcheck_server()
    except Exception:
        # Даже если health не смог стартануть — лучше увидеть причину в логах
        log.exception("Failed to start healthcheck server")
        raise

    session: aiohttp.ClientSession | None = None
    try:
        # 2) Настройки/БД
        settings = load_settings()
        await init_db()

        # 3) HTTP session для API
        timeout = aiohttp.ClientTimeout(total=10)
        session = aiohttp.ClientSession(timeout=timeout)

        # 4) Bot + Dispatcher
        bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode="HTML"),
        )
        dp = Dispatcher(storage=MemoryStorage())

        # 5) DI (как у тебя)
        dp["session"] = session
        dp["settings"] = settings
        dp["cache"] = AsyncCache(max_items=512)
        dp["semaphore"] = asyncio.Semaphore(10)
        dp["ui_state"] = {}
        dp["reply_menu_users"] = set()

        for router in get_routers():
            dp.include_router(router)

        await set_default_commands(bot)

        log.info("Bot started polling...")
        await dp.start_polling(bot)

    finally:
        # cleanup
        if session is not None:
            with suppress(Exception):
                await session.close()

        if health_runner is not None:
            with suppress(Exception):
                await health_runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())