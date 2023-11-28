from discord.ext import tasks
from discord.ext.commands import Cog, Bot


class TimeRule(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._5min_rule.start()
        self._1hr_rule.start()

    @tasks.loop(minutes=5)
    async def _5min_rule(self):
        channel = await self.bot.fetch_channel(1134222661753503775)
        await channel.purge(limit=100)

    @tasks.loop(hours=1)
    async def _1hr_rule(self):
        channel = await self.bot.fetch_channel(1134226399385890916)
        await channel.purge(limit=100)

    @_5min_rule.before_loop
    async def before_5min_rule(self):
        await self.bot.wait_until_ready()

    @_1hr_rule.before_loop
    async def before_1hr_rule(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(TimeRule(bot))
