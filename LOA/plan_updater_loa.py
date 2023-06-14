from discord import Embed
from discord.ext import tasks, commands
from datetime import datetime
from assets.functions import Plans


class PlanUpdaterCogLoa(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_plans_loa.start()

    @tasks.loop(minutes=5)
    async def update_plans_loa(self):
        loa_plan_log = self.bot.get_channel(990246941029990420)

        plans = Plans(704888699590279221)

        if plans.check() is None:
            return
        else:
            for i in plans.check():
                buyer = await self.bot.fetch_user(int(i[0]))
                ending = int(i[2])
                plan = i[3]
                setter = await self.bot.fetch_user(int(i[4]))
                plan_id = int(i[5])

                if int(datetime.now().timestamp()) > ending:
                    embed = Embed(title="Plan")
                    embed.add_field(name="Buyer", value=buyer, inline=False)
                    embed.add_field(name="Product", value=plan, inline=False)
                    await loa_plan_log.send(
                        "{}, {} has ended".format(setter.mention, plan_id), embed=embed
                    )
                    plans.remove(buyer, plan_id)
                else:
                    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(PlanUpdaterCogLoa(bot))
