from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from database import Database


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = getenv("DISCORD_TOKEN") or getenv("token")
DATABASE_URL = getenv("DATABASE_URL")
db = Database(DATABASE_URL)

orleans = 740584420645535775
vhf = 974028573893595146
