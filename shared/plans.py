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
        ending_time = today + timedelta(seconds=(parse_timespan(ends)))
        plan_id = randint(1, 100000)

        if ctx.guild.id == 925790259160166460:
            guild = 925790259160166460

        else:
            guild = 704888699590279221

        Plans(guild).add_plan(
            member, round(ending_time.timestamp()), plan, ctx.user, plan_id
        )

        ha_planlog = await self.bot.fetch_channel(956554797060866058)
        loa_planlog = await self.bot.fetch_channel(990246941029990420)
        planned = Embed(title="New plan", color=Color.blue())
        planned.add_field(
            name=member,
            value=f"**Plan Started:** <t:{round(today.timestamp())}:R>\n**Plan:** {plan}\n**Made by:** {ctx.user}\n**Ends when:** <t:{round(ending_time.timestamp())}:F>\n**Plan ID:** {plan_id}",
        )
        if ctx.guild.id == 925790259160166460:
            await ha_planlog.send(embed=planned)
            await ctx.followup.send(
                "Plan added to {}".format(ha_planlog.mention), ephemeral=True
            )
        else:
            await loa_planlog.send(embed=planned)
            await ctx.followup.send(
                "Plan added to {}".format(loa_planlog.mention), ephemeral=True
            )

    @Serverutil.command(description="End a plan if cancelled early")
    @Serverutil.checks.has_any_role(planmanager, operationmanager, loa_staff_team)
    async def end(self, ctx: Interaction, plan_id: int):
        await ctx.response.defer(ephemeral=True)
        if ctx.guild.id == hazead:
            guild = hazead

        else:
            guild = loa

        plan = Plans(guild)
        result = plan.get_plan(plan_id)

        if result == None:
            await ctx.followup.send("Invalid Plan ID.")

        else:
            plan.remove_plan(plan_id)
            await ctx.followup.send("Plan removed")


async def setup(bot: Bot):
    await bot.add_cog(
        plancog(bot), guilds=[Object(id=hazead), Object(id=loa), Object(id=lss)]
    )
