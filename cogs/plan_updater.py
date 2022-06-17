from nextcord.ext.commands import Cog
from nextcord import *
from nextcord.ext import tasks
from config import db
from datetime import *


class plan_updater_cog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_plans.start()

    @tasks.loop(minutes=5)
    async def update_plans(self):
        planlog = await self.bot.fetch_channel(956554797060866058)
        plan_msg = await planlog.fetch_message(956648242655920178)
        cur = db.execute(f"SELECT * FROM planData")
        results = cur.fetchall()

        if results ==None:
            planned = Embed(description="No Plans as of yet")
            await plan_msg.edit(embed=planned)

        else:
            planned = Embed(description="**Current plans**", color=Color.blue())
            for i in results:
                member = await self.bot.fetch_user(i[0])
                plan_start = i[1]
                ending = i[2]
                plan = i[3]
                setter = await self.bot.fetch_user(i[4])
                plan_id= i[5]

                planned.add_field(
                    name=member, value=f"**Plan Started:** {plan_start}\n**Plan:** {plan}\n**Made by:** {setter}\n**Ends when:** {ending}\n**Plan ID:** {plan_id}")
            await plan_msg.edit(embed=planned)


def setup(bot):
    bot.add_cog(plan_updater_cog(bot))
