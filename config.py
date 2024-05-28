from os import getenv
from sqlite3 import connect

from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("token")
WEBHOOK_URL_1 = getenv("chocola")  # Orleans
WEBHOOK_URL_2 = getenv("vanilla")  # Hazeads
TOKEN = getenv("token")
ORLEANS = getenv("orleans")

db = connect("database.db", check_same_thread=True)

hazead = 925790259160166460
orleans = 740584420645535775
vhf = 974028573893595146
