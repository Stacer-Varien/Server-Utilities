"""Import legacy message IDs and an optional SQLite database into Postgres."""

import argparse
import asyncio
import json
import sqlite3
from pathlib import Path

from config import BASE_DIR, DATABASE_URL, db


ACTIVE_TABLES = {
    "blacklistedServersData",
    "starboardPosts",
    "verificationLog",
}


def read_sqlite_database(path: Path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")

        tables = {}
        names = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        for (table_name,) in names:
            cursor = connection.execute(f' SELECT * FROM "{table_name}"')
            columns = [column[0] for column in cursor.description]
            tables[table_name] = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
        return tables
    finally:
        connection.close()


async def migrate(sqlite_path: Path | None) -> None:
    if not DATABASE_URL:
        raise SystemExit("Missing DATABASE_URL. Set a Neon Postgres connection string.")

    await db.connect()
    try:
        message_ids = await db.import_legacy_message_ids(BASE_DIR / "message_ids.txt")
        print(f"Legacy message_ids.txt migration complete ({message_ids} IDs inspected).")

        if sqlite_path is None:
            return

        tables = read_sqlite_database(sqlite_path)
        blacklist_rows = [
            (int(row["server_id"]), row.get("reason"))
            for row in tables.get("blacklistedServersData", [])
        ]
        starboard_rows = [
            (int(row["message_id"]), int(row["starboard_message_id"]))
            for row in tables.get("starboardPosts", [])
        ]
        verification_rows = [
            (int(row["user"]), int(row["message_id"]))
            for row in tables.get("verificationLog", [])
            if row.get("user") is not None and row.get("message_id") is not None
        ]

        print(f"Imported blacklist rows: {await db.import_legacy_blacklist_rows(blacklist_rows)}")
        print(f"Imported starboard rows: {await db.import_legacy_starboard_rows(starboard_rows)}")
        print(
            "Imported verification rows: "
            f"{await db.import_legacy_verification_rows(verification_rows)}"
        )

        archived = 0
        for table_name, rows in tables.items():
            if table_name in ACTIVE_TABLES:
                continue
            archived_rows = [
                (row_number, json.dumps(row, default=str))
                for row_number, row in enumerate(rows, start=1)
            ]
            archived += await db.import_legacy_rows(table_name, archived_rows)
        print(f"Archived unused SQLite rows: {archived}")
    finally:
        await db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sqlite-path",
        type=Path,
        help="Optional SQLite database to import into Neon.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(migrate(args.sqlite_path))
