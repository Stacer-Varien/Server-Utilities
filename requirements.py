import platform
import os

pip = "install -U pip"
packages = "install -U discord requests python-dotenv humanfriendly datetime git+https://github.com/Gorialis/jishaku"

pack = [pip, packages]

if platform.system() == "Linux":
    for i in pack:
        os.system('python3 -m pip ' + i)

elif platform.system() == "Windows":
    for i in pack:
        os.system('python.exe -m pip ' + i)