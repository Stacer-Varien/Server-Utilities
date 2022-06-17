from random import randint
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import has_role
from config import hazead, db
from datetime import *


class plancog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description='Add a plan a member claimed')
    @has_role(956634941066739772)
    async def add_plan(self, ctx: Interaction, member: Member = SlashOption(required=True), ends=SlashOption(required=True), plan=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        today = datetime.today().strftime('%Y-%m-%d')
        plan_id=randint(1,100000)
        claimee=ctx.user
        db.execute("INSERT OR IGNORE INTO planData (user_id, started, until, plans, set_by, plan_id) VALUES (?,?,?,?,?,?)",
                             (member.id, today, ends, plan, claimee.id, plan_id))
        
        db.commit()

        await ctx.followup.send("Plan added and will be updated in plan logs")
        self.bot.reload_extension('cogs.plan_updater')

    @slash(description='End a plan a member claimed if expired')
    @has_role(956634941066739772)
    async def end_plan(self, ctx: Interaction, plan_id=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        cur=db.execute(f"SELECT * FROM planData WHERE plan_id = {plan_id}")
        result=cur.fetchone()

        if result==0:
            await ctx.followup.send("Invalid Plan ID.")

        else:
            db.execute(f'DELETE FROM planData WHERE plan_id = {plan_id}')
            await ctx.followup.send("Plan removed")
            db.commit()

        self.bot.reload_extension('cogs.plan_updater')

def setup(bot):
    bot.add_cog(plancog(bot))
