from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.commands import Cog, Bot
from nextcord.ext import tasks

from assets.applications import AppButtons

HAZE_ADS = 925790259160166460


class application(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.reload_apps.start()
    
    @tasks.loop(minutes=2)
    async def reload_apps(self):
        embed=Embed()
        embed.description="Click on the available (grey buttons) positions that you wish to apply for"
        embed.color=Color.dark_blue()
        view=AppButtons()

        channel=await self.bot.fetch_channel(987658227485392967)
        msg = await channel.fetch_message(1045316538657423360)

        await msg.edit(embed=embed, view=view)

def setup(bot: Bot):
    bot.add_cog(application(bot))
