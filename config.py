from atexit import register
from os import getenv
from pathlib import Path
from sqlite3 import connect

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = getenv("DISCORD_TOKEN") or getenv("token")

DATABASE_PATH = Path(getenv("SERVER_UTILITIES_DB_PATH") or BASE_DIR / "database.db")
db = connect(DATABASE_PATH, check_same_thread=True)
db.execute("PRAGMA foreign_keys = ON")
db.executescript(
    """
    CREATE TABLE IF NOT EXISTS verificationLog (
        user INTEGER PRIMARY KEY,
        message_id INTEGER NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS blacklistedServersData (
        server_id INTEGER PRIMARY KEY,
        reason TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS starboardPosts (
        message_id INTEGER PRIMARY KEY,
        starboard_message_id INTEGER NOT NULL
    );
    """
)
db.commit()
register(db.close)

orleans = 740584420645535775
vhf = 974028573893595146
