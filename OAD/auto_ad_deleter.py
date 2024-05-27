from discord.ext import tasks
from discord.ext.commands import Cog, Bot


class TimeRule(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._10min_rule.start()
        self._1hr_rule.start()

    @tasks.loop(minutes=10)
    async def _10min_rule(self):
        channel = await self.bot.fetch_channel(1239498297908002900)
        await channel.purge(limit=100)

    @tasks.loop(hours=1)
    async def _1hr_rule(self):
        channel = await self.bot.fetch_channel(1239498385870819352)
        await channel.purge(limit=100)


async def setup(bot: Bot):
    await bot.add_cog(TimeRule(bot))
