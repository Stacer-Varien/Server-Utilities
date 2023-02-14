from discord import *
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import *
from assets.functions import Plans


class plan_updater_cog_loa(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.update_plans_loa.start()

    @tasks.loop(minutes=1)
    async def update_plans_loa(self):
        loa_plan_log = await self.bot.fetch_channel(990246941029990420)

        plans = Plans(704888699590279221)

        if plans.check_plans() == None:
            pass

        else:
            for i in plans.check_plans():
                buyer = await self.bot.fetch_user(i[0])
                ending = i[2]
                plan = i[3]
                setter = await self.bot.fetch_user(i[4])
                plan_id = i[5]

                if int(round(datetime.now().timestamp())) > int(ending):
                    embed = Embed(title="Plan")
                    embed.add_field(name="Buyer", value=buyer, inline=False)
                    embed.add_field(name="Product", value=plan, inline=False)
                    await loa_plan_log.send("{}, {} has ended".format(
                        setter.mention, plan_id),
                                            embed=embed)
                    plans.remove_plan(plan_id)
                else:
                    pass


async def setup(bot: Bot):
    await bot.add_cog(plan_updater_cog_loa(bot))
