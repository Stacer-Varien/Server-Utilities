from datetime import datetime
from assets.functions import Break
from discord.ext import tasks
from discord.ext.commands import Cog, Bot


class BreakUpdater(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_break.start()

    @tasks.loop(minutes=5)
    async def check_break(self):
        check_breaks = Break().check_breaks()
        loa = self.bot.get_guild(841671029066956831)  # Use get_guild instead of fetch_guild if possible
        break_role = loa.get_role(841682795277713498)
        break_channel = self.bot.get_channel(841676953613631499)  # Use get_channel instead of fetch_channel if possible

        for a in check_breaks:
            try:
                if int(round(datetime.now().timestamp())) > int(a[6]):
                    member = loa.get_member(a[0])  # Use get_member instead of fetch_member if possible

                    await member.remove_roles(break_role, reason="Break has ended")

                    Break(member).remove()

                    await break_channel.send(f"{member.mention}, your break has ended")
            except Exception:
                continue


async def setup(bot: Bot):
    await bot.add_cog(BreakUpdater(bot))
