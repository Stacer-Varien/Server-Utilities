import asyncio
import tempfile
import unittest
from pathlib import Path

from database import Database, SCHEMA


class FakeAcquire:
    def __init__(self, connection):
        self.connection = connection

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, exc_type, exc, traceback):
        return False


class FakeConnection:
    def __init__(self):
        self.executemany_arguments = []

    async def executemany(self, query, arguments):
        self.executemany_arguments = list(arguments)


class FakePool:
    def __init__(self, connection):
        self.connection = connection

    def acquire(self):
        return FakeAcquire(self.connection)


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_legacy_message_ids_are_deduplicated_and_invalid_lines_ignored(self):
        connection = FakeConnection()
        database = Database("postgresql://unused")
        database.pool = FakePool(connection)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "message_ids.txt"
            path.write_text("123\nnot-an-id\n123\n456\n", encoding="utf-8")

            inspected = await database.import_legacy_message_ids(path)

        self.assertEqual(inspected, 2)
        self.assertEqual(
            sorted(connection.executemany_arguments), [(123,), (456,)]
        )

    async def test_missing_legacy_file_is_a_noop(self):
        database = Database("postgresql://unused")
        database.pool = FakePool(FakeConnection())

        inspected = await database.import_legacy_message_ids(
            Path("does-not-exist-message-ids.txt")
        )

        self.assertEqual(inspected, 0)

    async def test_database_requires_a_url(self):
        with self.assertRaisesRegex(RuntimeError, "DATABASE_URL"):
            await Database(None).connect()

    def test_schema_uses_postgres_safe_table_names(self):
        self.assertIn("verification_log", SCHEMA)
        self.assertIn("blacklisted_servers", SCHEMA)
        self.assertIn("starboard_posts", SCHEMA)
        self.assertIn("legacy_sqlite_rows", SCHEMA)
        self.assertNotIn("verificationLog", SCHEMA)
        self.assertNotIn("blacklistedServersData", SCHEMA)


if __name__ == "__main__":
    asyncio.run(unittest.main())
