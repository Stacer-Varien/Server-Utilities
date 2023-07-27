from datetime import datetime, timedelta
from discord.ext.commands import Cog, Bot
from discord.ext import tasks


class timerrule(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._5min_rule.start()

    @tasks.loop(minutes=5)
    async def _5min_rule(self):
        channel = await self.bot.fetch_channel(1134222661753503775)
        now = datetime.utcnow()
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                if now - message.created_at > timedelta(minutes=5):
                    await message.delete(delay=0.5)
        except:
            pass

    @tasks.loop(hours=1)
    async def _1hr_rule(self):
        channel = await self.bot.fetch_channel(1134226399385890916)
        now = datetime.utcnow()
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                if now - message.created_at > timedelta(hours=1):
                    await message.delete(delay=0.5)
        except:
            pass


async def setup(bot: Bot):
    await bot.add_cog(timerrule(bot))
