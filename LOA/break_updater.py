from datetime import *
from assets.functions import check_loa_breaks, remove_loa_break
from nextcord.ext import tasks
from nextcord.ext.commands import Cog, Bot

from config import db


class break_updater(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_break.start()

    @tasks.loop(seconds=5)
    async def check_break(self):
        check_breaks = check_loa_breaks()
        loa = await self.bot.fetch_guild(841671029066956831)
        break_role = loa.get_role(841682795277713498)
        break_channel = await loa.fetch_channel(841676953613631499)

        for a in check_breaks:
            try:
                if int(round(datetime.now().timestamp())) > int(a[7]):
                    member = await loa.fetch_member(a[0])

                    await member.remove_roles(break_role, reason="Break has ended")

                    remove_loa_break(member)

                    await break_channel.send("{}, your break has ended".format(member.mention))
            except:
                continue


def setup(bot: Bot):
    bot.add_cog(break_updater(bot))
