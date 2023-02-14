from discord import *
from discord.ext.commands import Cog, Bot


class errors(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(
            self, ctx: Interaction, error: app_commands.AppCommandError):
        embed = Embed(description=error, color=Color.red())
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(errors(bot))
