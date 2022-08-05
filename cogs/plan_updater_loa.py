from nextcord import *
from nextcord.ext import tasks
from nextcord.ext.commands import Cog

from config import db


class plan_updater_cog_loa(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_plans_loa.start()

    @tasks.loop(minutes=1)
    async def update_plans_loa(self):
        loa_plan_log = await self.bot.fetch_channel(990246941029990420)
        loa_plan_msg = await loa_plan_log.fetch_message(991288734408507442)

        cur = db.execute(
            f"SELECT * FROM planData where server_id = ?", (841671029066956831,))
        results = cur.fetchall()

        if results == None:
            planned = Embed(description="No Plans as of yet")
            await loa_plan_msg.edit(embed=planned)

        else:
            planned = Embed(description='Current Plans', color=Color.blue())
            for i in results:
                member = await self.bot.fetch_user(i[0])
                plan_start = i[1]
                ending = i[2]
                plan = i[3]
                setter = await self.bot.fetch_user(i[4])
                plan_id = i[5]

                planned.add_field(
                    name=member,
                    value=f"**Plan Started:** <t:{plan_start}:R>\n**Plan:** {plan}\n**Made by:** {setter}\n**Ends when:** <t:{ending}:F>\n**Plan ID:** {plan_id}")
            await loa_plan_msg.edit(embed=planned)


def setup(bot):
    bot.add_cog(plan_updater_cog_loa(bot))
