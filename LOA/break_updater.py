from datetime import datetime
from assets.functions import Break
from discord.ext import tasks
from discord.ext.commands import Cog, Bot


class break_updater(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_break.start()

    @tasks.loop(minutes=5)
    async def check_break(self):
        check_breaks = Break().check_breaks()
        loa = await self.bot.fetch_guild(841671029066956831)
        break_role = loa.get_role(841682795277713498)
        break_channel = await loa.fetch_channel(841676953613631499)

        for a in check_breaks:
            try:
                if int(round(datetime.now().timestamp())) > int(a[6]):
                    member = await loa.fetch_member(a[0])

                    await member.remove_roles(break_role, reason="Break has ended")

                    Break(member).remove()

                    await break_channel.send(
                        "{}, your break has ended".format(member.mention)
                    )
            except:
                continue


async def setup(bot: Bot):
    await bot.add_cog(break_updater(bot))
