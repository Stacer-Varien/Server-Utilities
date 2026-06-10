from pathlib import Path
from subprocess import check_call
from sys import executable

ROOT = Path(__file__).resolve().parent

check_call([executable, "-m", "pip", "install", "--upgrade", "pip"])
check_call([executable, "-m", "pip", "install", "-r", ROOT / "requirements.txt"])
