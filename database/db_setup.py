import os
import json
import datetime
import aiosqlite


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "cat_bot.db")


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS cat_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                facts TEXT NOT NULL DEFAULT '[]',
                current_index INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS http_cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                expires_at REAL
            )
            """
        )
        await db.commit()


async def get_user_facts(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM cat_facts WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                facts = []
                await db.execute(
                    """
                    INSERT INTO cat_facts (user_id, facts, current_index, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        json.dumps(facts),
                        0,
                        datetime.datetime.utcnow().isoformat(),
                    ),
                )
                await db.commit()
                return {"facts": facts, "current_index": 0}

            return {
                "facts": json.loads(row["facts"]) if row["facts"] else [],
                "current_index": row["current_index"],
            }


async def update_user_facts(user_id: int, facts: list, current_index: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            UPDATE cat_facts
            SET facts = ?, current_index = ?
            WHERE user_id = ?
            """,
            (json.dumps(facts), current_index, user_id),
        )
        await db.commit()


async def get_cache_value(key: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT value, expires_at FROM http_cache WHERE key = ?",
            (key,),
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            expires_at = row["expires_at"]
            if expires_at and expires_at < datetime.datetime.utcnow().timestamp():
                await db.execute("DELETE FROM http_cache WHERE key = ?", (key,))
                await db.commit()
                return None
            return row["value"]


async def set_cache_value(key: str, value: str, ttl: int | None):
    expires_at = None
    if ttl:
        expires_at = datetime.datetime.utcnow().timestamp() + ttl

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO http_cache (key, value, expires_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, expires_at = excluded.expires_at
            """,
            (key, value, expires_at),
        )
        await db.commit()
