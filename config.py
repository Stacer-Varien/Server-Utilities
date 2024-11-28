from os import getenv
from sqlite3 import connect
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("token")

db = connect("database.db", check_same_thread=True)

orleans = 740584420645535775
vhf = 974028573893595146
