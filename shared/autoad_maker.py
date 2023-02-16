from datetime import timedelta
from sys import version_info as py_version
from time import time
from collections import OrderedDict
from json import load
from discord import Embed, Interaction, Color, Object
from discord import app_commands as Serverutil
from discord.ext.commands import GroupCog, Bot
from config import lss, hazead, loa, orleans

class autoadcog(GroupCog, name='automod'):
    def __init__(self, bot:Bot):
        self.bot=bot

    @Serverutil.command(description="Create an autoad and starts it")
    @Serverutil.checks.has_any_role()