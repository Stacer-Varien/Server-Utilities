from os import listdir

from discord import Intents, Object
from discord.ext.commands import Bot, when_mentioned_or

from config import TOKEN, lss, loa, orleans, hazead

intents = Intents().all()
intents.presences = False
intents.voice_states = False
intents.auto_moderation = False
intents.guild_scheduled_events = False


class ServerUtilities(Bot):
    async def setup_hook(self):
        await bot.load_extension("jishaku")
        for filename in listdir("./HA"):
            if filename.endswith(".py"):
                await bot.load_extension(f"HA.{filename[:-3]}")
                print(f"{filename} loaded")
            else:
                print(f"Unable to load {filename[:-3]}")

        for filename in listdir("./LOA"):
            if filename.endswith(".py"):
                await bot.load_extension(f"LOA.{filename[:-3]}")
                print(f"{filename} loaded")
            else:
                print(f"Unable to load {filename[:-3]}")

        for filename in listdir("./shared"):
            if filename.endswith(".py"):
                await bot.load_extension(f"shared.{filename[:-3]}")
                print(f"{filename} loaded")
            else:
                print(f"Unable to load {filename[:-3]}")


bot = ServerUtilities(
    intents=intents,
    command_prefix=when_mentioned_or("su!", "SU!", "Su!", "su", "SU", "sU"),
)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))
    for guild in [
        Object(id=lss),
        Object(id=loa),
        Object(id=orleans),
        Object(id=hazead),
    ]:
        await bot.tree.sync(guild=guild)


bot.run(TOKEN)
