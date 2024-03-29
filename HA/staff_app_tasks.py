from discord import Embed, Color
from discord.ext import tasks
from discord.ext.commands import Cog, Bot

from assets.applications import AppButtons

class ApplicationCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.reload_apps.start()

    @tasks.loop(hours=24)
    async def reload_apps(self):
        embed = Embed()
        embed.description = (
            "Click on the available (grey buttons) positions that you wish to apply for"
        )
        embed.color = Color.dark_blue()
        view = AppButtons()

        channel = await self.bot.fetch_channel(987658227485392967)
        msg = await channel.fetch_message(1045316538657423360)

        await msg.edit(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(ApplicationCog(bot))
