from nextcord import *
from nextcord.ext import tasks
from nextcord.ext.commands import Cog, Bot
from datetime import *
from config import db


class plan_updater_cog_loa(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.update_plans_loa.start()

    @tasks.loop(minutes=1)
    async def update_plans_loa(self):
        loa_plan_log = await self.bot.fetch_channel(990246941029990420)

        cur = db.execute(
            f"SELECT * FROM planData where server_id = ?", (704888699590279221,))
        results = cur.fetchall()

        if results == None:
            pass

        else:
            for i in results:
                buyer=await self.bot.fetch_user(i[0])
                ending = i[2]
                plan=i[3]
                setter = await self.bot.fetch_user(i[4])
                plan_id = i[5]

                if int(ending) > int(round(datetime.now().timestamp())):
                    embed=Embed(title="Plan")
                    embed.add_field(name="Buyer", value=buyer, inline=False)
                    embed.add_field(name="Product", value=plan, inline=False)
                    await loa_plan_log.send("{}, {} has ended".format(setter.mention, plan_id), embed=embed)
                    db.execute(
                        'DELETE FROM planData WHERE plan_id= ? AND server_id= ?', (plan_id, 704888699590279221,))
                    db.commit()
                    


def setup(bot: Bot):
    bot.add_cog(plan_updater_cog_loa(bot))
