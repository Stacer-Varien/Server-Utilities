import os
from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext import commands
from config import TOKEN, lss, loa, orleans, hazead


intents = Intents().all()
intents.presences = False
intents.voice_states = False
intents.auto_moderation = False
intents.guild_scheduled_events = False


class ServerUtilities(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command("help")

    async def setup_extensions(self, path, package):
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"{package}.{filename[:-3]}")
                    print(f"{filename} loaded")
                except commands.ExtensionError as e:
                    print(f"Failed to load {filename[:-3]}: {e}")
            else:
                print(f"Unable to load {filename[:-3]}")

    async def on_ready(self):
        print("Connected to bot: {}".format(self.user.name))
        print("Bot ID: {}".format(self.user.id))
        for guild_id in [lss, loa, orleans, hazead]:
            guild = self.get_guild(guild_id)
            if guild is not None:
                await self.tree.sync(guild=guild)

    async def setup_hook(self):
        await self.load_extension('jishaku')
        await self.setup_extensions("./HA", "HA")
        await self.setup_extensions("./LOA", "LOA")
        await self.setup_extensions("./shared", "shared")


bot = ServerUtilities(
    intents=intents,
    command_prefix=when_mentioned_or("su!", "SU!", "Su!", "su", "SU", "sU"),
)


@bot.event
async def on_connect():
    print("Bot connected to Discord")


@bot.event
async def on_disconnect():
    print("Bot disconnected from Discord")


@bot.event
async def on_resumed():
    print("Bot resumed")


bot.run(TOKEN)
