from datetime import datetime

from discord import Embed
from discord.ext import tasks, commands

from assets.functions import Plans

class PlanUpdaterCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_plans_ha.start()


    @tasks.loop(minutes=5)
    async def update_plans_ha(self):
        ha_planlog = await self.bot.fetch_channel(956554797060866058)

        plans = Plans(925790259160166460)

        if plans.check() is None:
            return

        for i in plans.check():
            buyer = await self.bot.fetch_user(i[0])
            ending = i[2]
            plan = i[3]
            setter = await self.bot.fetch_user(i[4])
            plan_id = i[5]

            if int(round(datetime.now().timestamp())) > int(ending):
                embed = Embed(title="Plan")
                embed.add_field(name="Buyer", value=buyer, inline=False)
                embed.add_field(name="Product", value=plan, inline=False)
                embed.add_field(name="Ending", value=ending, inline=False)
                await ha_planlog.send(
                    "{}, {} has ended".format(setter.mention, plan_id), embed=embed
                )
                plans.remove(buyer, plan_id)
                return



    @update_plans_ha.before_loop
    async def before_update_plans_ha(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(PlanUpdaterCog(bot))
