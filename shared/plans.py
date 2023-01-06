from datetime import *
from random import randint

from humanfriendly import parse_timespan
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import has_any_role
from nextcord.ext.commands import Cog, Bot

from assets.functions import add_plan, get_plan, remove_plan

planmanager = 956634941066739772
operationmanager = 841671956999045141
loa_staff_team = 706750926320566345


class plancog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash(description="Make plan command", guild_ids=[925790259160166460, 704888699590279221, 841671029066956831])
    async def plan(self, ctx:Interaction):
        pass

    @plan.subcommand(description='Add a plan a member claimed')
    @has_any_role(planmanager, operationmanager, loa_staff_team)
    async def add(self, ctx: Interaction, member: Member = SlashOption(required=True),
                       ends=SlashOption(description="Example: 1m (1 minute), 3w (3 weeks), 2y (2 years)",
                                        required=True), plan=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        today = datetime.now()
        ending_time = today + timedelta(seconds=(parse_timespan(ends)))
        plan_id = randint(1, 100000)
        claimee = ctx.user
        claimer = await self.bot.fetch_user(member.id)

        if ctx.guild.id == 925790259160166460:
            guild = 925790259160166460

        else:
            guild = 704888699590279221
        
        add_plan(member.id, round(ending_time.timestamp()), plan, claimee.id, plan_id, guild)

        ha_planlog = await self.bot.fetch_channel(956554797060866058)
        loa_planlog = await self.bot.fetch_channel(990246941029990420)
        planned=Embed(title="New plan", color=Color.blue())
        planned.add_field(
            name=member,
            value=f"**Plan Started:** <t:{round(today.timestamp())}:R>\n**Plan:** {plan}\n**Made by:** {ctx.user}\n**Ends when:** <t:{round(ending_time.timestamp())}:F>\n**Plan ID:** {plan_id}")
        if ctx.guild.id == 925790259160166460:
            await ha_planlog.send(embed=planned)
            await ctx.followup.send("Plan added to {}".format(ha_planlog.mention), ephemeral=True)
        else:
            await loa_planlog.send(embed=planned)
            await ctx.followup.send("Plan added to {}".format(loa_planlog.mention), ephemeral=True)


    @plan.subcommand(description='End a plan a member cancelled')
    @has_any_role(planmanager, operationmanager, loa_staff_team)
    async def end(self, ctx: Interaction, plan_id=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        if ctx.guild.id == 925790259160166460:
            guild = 925790259160166460

        else:
            guild = 704888699590279221
        
        result = get_plan(plan_id, guild)

        if result == None:
            await ctx.followup.send("Invalid Plan ID.")

        else:
            remove_plan(plan_id, guild)
            await ctx.followup.send("Plan removed")

def setup(bot: Bot):
    bot.add_cog(plancog(bot))
