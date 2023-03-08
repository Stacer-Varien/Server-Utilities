from discord import *
from discord.ext.commands import Cog, Bot
import traceback


class errors(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(
            self, ctx: Interaction, error: app_commands.AppCommandError):
        traceback_error = traceback.format_exception(error, error,
                                                     error.__traceback__)
        with open('errors.txt', 'a') as f:
            f.writelines(f"{traceback_error}\n\n")


async def setup(bot: Bot):
    await bot.add_cog(errors(bot))
