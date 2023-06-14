from datetime import datetime
from discord.ext import tasks, commands
from assets.functions import Break


class BreakUpdater(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_break.start()

    @tasks.loop(minutes=5)
    async def check_break(self):
        check_breaks = Break().check_breaks()
        guild_id = 841671029066956831
        break_role_id = 841682795277713498
        break_channel_id = 841676953613631499

        try:
            guild = self.bot.get_guild(guild_id)
            break_role = guild.get_role(break_role_id)
            break_channel = self.bot.get_channel(break_channel_id)

            if guild is None or break_role is None or break_channel is None:
                return

            for a in check_breaks:
                try:
                    if int(round(datetime.now().timestamp())) > int(a[6]):
                        member = guild.get_member(int(a[0]))

                        if member is not None:
                            await member.remove_roles(break_role, reason="Break has ended")
                            Break(member).remove()
                            await break_channel.send(f"{member.mention}, your break has ended")
                except Exception:
                    continue
        except Exception as e:
            print(f"Error occurred in check_break: {e}")

    @check_break.before_loop
    async def before_check_break(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(BreakUpdater(bot))
