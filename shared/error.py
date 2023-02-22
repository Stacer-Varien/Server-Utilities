from discord import *
from discord.ext.commands import Cog, Bot
import traceback

class errors(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(
            self, ctx: Interaction, error: app_commands.AppCommandError):
        embed = Embed(description=error, color=Color.red())
        with open('errors.txt', 'a') as f:
            f.writelines(
                f"{traceback.format_exception(type(error), error, error.__traceback__)}\n\n"
            )
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(errors(bot))
