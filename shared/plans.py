from datetime import *
from random import randint

from humanfriendly import parse_timespan
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import has_any_role
from nextcord.ext.commands import Cog, Bot

from config import db

planmanager = 956634941066739772
operationmanager = 841671956999045141
loa_staff_team = 706750926320566345


class plancog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash(description='Add a plan a member claimed')
    @has_any_role(planmanager, operationmanager, loa_staff_team)
    async def addplan(self, ctx: Interaction, member: Member = SlashOption(required=True),
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
        db.execute(
            "INSERT OR IGNORE INTO planData (user_id, started, until, plans, set_by, plan_id, server_id) VALUES (?,?,?,?,?,?,?)",
            (claimer.id, round(today.timestamp()), round(ending_time.timestamp()), plan, claimee.id, plan_id, guild,))

        db.commit()

        await ctx.followup.send("Plan added and will be updated in plan logs")

    @slash(description='End a plan a member claimed if expired')
    @has_any_role(planmanager, operationmanager, loa_staff_team)
    async def endplan(self, ctx: Interaction, plan_id=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        if ctx.guild.id == 925790259160166460:
            guild = 925790259160166460

        else:
            guild = 704888699590279221
        cur = db.execute("SELECT * FROM planData WHERE plan_id = ? AND server_id = ?", (plan_id, guild,))
        result = cur.fetchone()

        if result == 0:
            await ctx.followup.send("Invalid Plan ID.")

        else:
            db.execute('DELETE FROM planData WHERE plan_id= ? AND server_id= ?', (plan_id, guild,))
            db.commit()
            await ctx.followup.send("Plan removed")


def setup(bot: Bot):
    bot.add_cog(plancog(bot))
