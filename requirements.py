import os
import platform

pip = "install -U pip"
packages = "install -U discord.py requests python-dotenv Pillow humanfriendly datetime tabulate jishaku"

pack = [pip, packages]

if platform.system() == "Linux":
    for i in pack:
        os.system("python3 -m pip " + i)

elif platform.system() == "Windows":
    for i in pack:
        os.system("python.exe -m pip " + i)
