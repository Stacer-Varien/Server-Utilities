from datetime import datetime, timedelta
from random import randint
from humanfriendly import parse_timespan
from discord import *
from discord import app_commands as Serverutil
from discord.ext.commands import GroupCog, Bot
from config import hazead, loa, lss

from assets.functions import Plans

planmanager = 956634941066739772
operationmanager = 841671956999045141
loa_staff_team = 706750926320566345


class plancog(GroupCog, name="plan"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Add a plan a member claimed")
    @Serverutil.describe(ends="Example: 1m (1 minute), 3w (3 weeks), 2y (2 years)")
    @Serverutil.checks.has_any_role(planmanager, operationmanager, loa_staff_team)
    async def add(self, ctx: Interaction, member: Member, ends: str, plan: str):
        await ctx.response.defer(ephemeral=True)
        today = datetime.now()
        ending_time = today + timedelta(seconds=parse_timespan(ends))
        plan_id = randint(1, 100000)

        if ctx.guild.id == 925790259160166460:
            guild_id = 925790259160166460
            plan_log_channel_id = 956554797060866058
        else:
            guild_id = 704888699590279221
            plan_log_channel_id = 990246941029990420

        Plans(guild_id).add(member, round(ending_time.timestamp()), plan, ctx.user, plan_id)

        plan_log_channel = self.bot.get_channel(plan_log_channel_id)
        planned = Embed(title="New Plan", color=Color.blue())
        planned.add_field(
            name=str(member),
            value=(
                f"**Plan Started:** <t:{round(today.timestamp())}:R>\n"
                f"**Plan:** {plan}\n"
                f"**Made by:** {ctx.user}\n"
                f"**Ends when:** <t:{round(ending_time.timestamp())}:F>\n"
                f"**Plan ID:** {plan_id}"
            ),
        )
        await plan_log_channel.send(embed=planned)
        await ctx.followup.send(
                "Plan added to {}".format(plan_log_channel.mention), ephemeral=True
            )

    @Serverutil.command(description="End a plan if cancelled early")
    @Serverutil.checks.has_any_role(planmanager, operationmanager, loa_staff_team)
    async def end(self, ctx: Interaction, plan_id: int):
        await ctx.response.defer(ephemeral=True)
        if ctx.guild.id == hazead:
            guild_id = hazead
        else:
            guild_id = loa

        plan = Plans(guild_id)
        result = plan.get(plan_id)

        if result is None:
            await ctx.followup.send("Invalid Plan ID.")

        else:
            plan.remove(plan_id)
            await ctx.followup.send("Plan removed")

async def setup(bot: Bot):
    await bot.add_cog(
        plancog(bot), guilds=[Object(id=hazead), Object(id=loa), Object(id=lss)]
    )
