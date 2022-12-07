from nextcord import *
from nextcord.ext.commands import Cog, Bot

class errors(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationCheckFailure):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)



def setup(bot: Bot):
    bot.add_cog(errors(bot))
