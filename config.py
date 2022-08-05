from os import getenv
from sqlite3 import connect

from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("token")
HA_WEBHOOK = getenv("ha_webhook")
HAZE_WEBHOOK = getenv("haze_webhook")
SHU = getenv("safety_webhhook_unlimited")
SHC = getenv("safety_webhhook_community")

db = connect('database.db')

# server
hazead = 925790259160166460

# owner
varien = 597829930964877369
