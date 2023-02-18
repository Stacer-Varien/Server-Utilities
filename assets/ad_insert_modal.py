from random import randint
from discord import ui, TextStyle, Interaction, Embed, Color
from discord.ext.commands import Bot
from assets.functions import Plans


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class Ad_Insert(ui.Modal):
    def __init__(self, bot:Bot, buyer_id:int, name:str, looping:str, ending:int, channels:str):
        self.buyer_id=buyer_id
        self.name=name
        self.looping=looping
        self.ending=ending
        self.channels=channels
        self.bot=bot

        super().__init__(
            "Ad Model")

        self.ad_insert = ui.TextInput(
                                        label="Ad",
                                        min_length=4,
                                        max_length=2000,
                                        required=True,
                                        placeholder="Insert the ad. Make sure there is no public pings",
                                        style=TextStyle.paragraph
                                        )
        self.add_item(self.ad_insert)

    async def callback(self, ctx: Interaction) -> None:

        with open(f"{self.name}.txt", 'w') as f:
            f.writelines(self.ad_insert.value)

        extension=f"""

from discord.ext.commands import Cog, Bot
from discord.ext import tasks
from discord import *


class {self.name}(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.post.start()

    @tasks.loop({self.looping})
    async def post(self):
        channels=[{self.channels.replace(' ', ',').split(',')}]
        with open("autopost/{self.name}.txt") as f:
            content = "".join(f.readlines())
        
        for a in channels:
          channel = await self.bot.fetch_channel(a)
          await channel.send(content)

async def setup(bot:Bot):
    await bot.add_cog({self.name}(bot))
        """

        with open(f"autopost/{self.name}.py", 'w') as f:
            f.writelines(extension)

        if ctx.guild.id == 925790259160166460:
            guild = 925790259160166460

        else:
            guild = 704888699590279221

        plan_id = randint(1, 100000)
        buyer=await self.bot.fetch_user(self.buyer_id)

        Plans(guild).add_plan(buyer, self.ending, f"Autoad {self.name}", ctx.user, plan_id)

        embed=Embed()
        embed.description="Auto ad {} has been made and started. A plan has already been made and sent to <#990246941029990420>"
        embed.add_field(name="Buyer", value=buyer, inline=True)
        embed.add_field(name="Looping time", value=self.looping, inline=False)
        embed.add_field(name="Channels", value=self.channels, inline=False)
        embed.add_field(name="Ending", value= f"<t:{self.ending}:F>", inline=False)
        embed.add_field(name="Plan ID", value=plan_id, inline=False)
        embed.color=Color.random()

        await self.bot.load_extension(f'autopost.{self.name}')
        channel= await self.bot.fetch_channel(990246941029990420)
        await channel.send(embed=embed)
        return await ctx.channel.send(embed=embed)
