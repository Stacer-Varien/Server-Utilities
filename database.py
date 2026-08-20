"""Async Postgres persistence for Server Utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import asyncpg


SCHEMA = """
CREATE TABLE IF NOT EXISTS verification_log (
    user_id BIGINT PRIMARY KEY,
    message_id BIGINT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS blacklisted_servers (
    server_id BIGINT PRIMARY KEY,
    reason TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS starboard_posts (
    message_id BIGINT PRIMARY KEY,
    starboard_message_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS legacy_sqlite_rows (
    table_name TEXT NOT NULL,
    row_number INTEGER NOT NULL,
    data JSONB NOT NULL,
    PRIMARY KEY (table_name, row_number)
);
"""


class Database:
    def __init__(self, url: str | None):
        self.url = url
        self.pool: asyncpg.Pool | None = None

    def _require_pool(self) -> asyncpg.Pool:
        if self.pool is None:
            raise RuntimeError("The database has not been initialized.")
        return self.pool

    async def connect(self) -> None:
        if self.pool is not None:
            return
        if not self.url:
            raise RuntimeError(
                "Missing DATABASE_URL. Set a Neon Postgres connection string."
            )

        pool = await asyncpg.create_pool(
            self.url,
            min_size=1,
            max_size=3,
            command_timeout=15,
        )
        try:
            async with pool.acquire() as connection:
                await connection.execute(SCHEMA)
        except Exception:
            await pool.close()
            raise
        self.pool = pool

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def import_legacy_message_ids(self, path: Path) -> int:
        """Import the legacy starboard source IDs without creating duplicates."""
        if not path.exists():
            return 0

        message_ids = {
            int(value.strip())
            for value in path.read_text(encoding="utf-8").splitlines()
            if value.strip().isdigit()
        }
        if not message_ids:
            return 0

        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.executemany(
                """
                INSERT INTO starboard_posts (message_id, starboard_message_id)
                VALUES ($1, 0)
                ON CONFLICT (message_id) DO NOTHING
                """,
                ((message_id,) for message_id in message_ids),
            )
        return len(message_ids)

    async def import_legacy_blacklist_rows(
        self, rows: list[tuple[int, str | None]]
    ) -> int:
        if not rows:
            return 0
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.executemany(
                """
                INSERT INTO blacklisted_servers (server_id, reason)
                VALUES ($1, COALESCE($2, ''))
                ON CONFLICT (server_id) DO NOTHING
                """,
                rows,
            )
        return len(rows)

    async def import_legacy_starboard_rows(
        self, rows: list[tuple[int, int]]
    ) -> int:
        if not rows:
            return 0
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.executemany(
                """
                INSERT INTO starboard_posts (message_id, starboard_message_id)
                VALUES ($1, $2)
                ON CONFLICT (message_id) DO NOTHING
                """,
                rows,
            )
        return len(rows)

    async def import_legacy_verification_rows(
        self, rows: list[tuple[int, int]]
    ) -> int:
        if not rows:
            return 0
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.executemany(
                """
                INSERT INTO verification_log (user_id, message_id)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
                """,
                rows,
            )
        return len(rows)

    async def import_legacy_rows(
        self, table_name: str, rows: list[tuple[int, str]]
    ) -> int:
        if not rows:
            return 0
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.executemany(
                """
                INSERT INTO legacy_sqlite_rows (table_name, row_number, data)
                VALUES ($1, $2, $3::jsonb)
                ON CONFLICT (table_name, row_number) DO NOTHING
                """,
                ((table_name, row_number, data) for row_number, data in rows),
            )
        return len(rows)

    async def add_verification_request(self, user_id: int, message_id: int) -> None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO verification_log (user_id, message_id)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
                """,
                user_id,
                message_id,
            )

    async def get_request_user_id(self, message_id: int) -> int | None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            return await connection.fetchval(
                "SELECT user_id FROM verification_log WHERE message_id = $1",
                message_id,
            )

    async def has_request_for_message(self, message_id: int) -> bool:
        return await self.get_request_user_id(message_id) is not None

    async def has_request_for_user(self, user_id: int) -> bool:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            return (
                await connection.fetchval(
                    "SELECT 1 FROM verification_log WHERE user_id = $1",
                    user_id,
                )
                is not None
            )

    async def remove_verification_request(self, message_id: int) -> None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                "DELETE FROM verification_log WHERE message_id = $1", message_id
            )

    async def get_blacklisted_server_ids(self) -> list[int]:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch("SELECT server_id FROM blacklisted_servers")
        return [row["server_id"] for row in rows]

    async def add_blacklisted_server(self, server_id: int, reason: str) -> None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO blacklisted_servers (server_id, reason)
                VALUES ($1, $2)
                ON CONFLICT (server_id) DO NOTHING
                """,
                server_id,
                reason,
            )

    async def remove_blacklisted_server(self, server_id: int) -> None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                "DELETE FROM blacklisted_servers WHERE server_id = $1", server_id
            )

    async def has_starboard_post(self, message_id: int) -> bool:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            return (
                await connection.fetchval(
                    "SELECT 1 FROM starboard_posts WHERE message_id = $1",
                    message_id,
                )
                is not None
            )

    async def record_starboard_post(
        self, message_id: int, starboard_message_id: int
    ) -> None:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO starboard_posts (message_id, starboard_message_id)
                VALUES ($1, $2)
                ON CONFLICT (message_id) DO NOTHING
                """,
                message_id,
                starboard_message_id,
            )

    async def export_data(self) -> dict[str, list[dict[str, Any]]]:
        pool = self._require_pool()
        async with pool.acquire() as connection:
            tables = {
                "verification_log": "SELECT user_id, message_id FROM verification_log",
                "blacklisted_servers": "SELECT server_id, reason FROM blacklisted_servers",
                "starboard_posts": "SELECT message_id, starboard_message_id FROM starboard_posts",
                "legacy_sqlite_rows": "SELECT table_name, row_number, data FROM legacy_sqlite_rows",
            }
            result = {}
            for name, query in tables.items():
                result[name] = [dict(row) for row in await connection.fetch(query)]
            return result
