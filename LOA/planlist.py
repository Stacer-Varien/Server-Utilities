from discord import (
    CategoryChannel,
    Color,
    Embed,
    Interaction,
    Object,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog
from assets.menus import ProductSelect
from config import lss


class pricelistcog(GroupCog, name="pricelist"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Get a list of LOA coin pricelist")
    async def loacoins(self, ctx: Interaction):
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)

        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                view = ProductSelect()
                embed = Embed()
                embed.color = Color.blue()
                embed.description = "Use the dropmenu below to view a package"
                await ctx.response.send_message(embed=embed, view=view)

    @Serverutil.command(description="Get a list of LOA coin pricelist")
    async def paidplans(self, ctx: Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                embed = Embed(color=Color.blue())
                embed.title = "Paid plans"
                embed.description = """
$3 Nitro:
- Giveaway with prize provided by us (or by your side if you are willing to), 7 days
- Custom Channel with Shoutout Ping + Partner Ping
- 10000 LOA Coins
- Premium Role for a month

$10 Nitro:
- Fully customisable package base on your server type and size 
What you can get for getting any of our plans:
- ⭐ Shiny high up Buyers role
- 🌟 Giveaway bonus entries
"""

    @Serverutil.command(description="Get a list of LOA booster plans")
    async def boosts(self, ctx: Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                embed = Embed(color=Color.blue())
                embed.title = "Booster plans"
                embed.description = """
♦️1 Boost
- Premium Membership until your boosts end
- Shoutout with Shoutout Ping + Partner Ping
- 5000 LOA Coins
- LOA Booster role
- Massive thank you
- Giveaway bonus entries

♦️♦️ 2 Boosts

- All above perks
- 8000 LOA Coins
- Auto advertisement in Open Network every 4 hours
- Legendary Booster Role

♦️ ♦️ ♦️ 3 boosts
-All above perks
-Auto Advertisement in Open Network upgrade to every 1 hour (worth 40k LOA Coins)
-12000 LOA Coins 
"""
                await ctx.followup.send(embed=embed)

    @Serverutil.command(name="discounts-and-gifting",description="...")
    async def discounts_and_gifts(self, ctx:Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:        
                embed=Embed()
                embed.color=Color.blue()
                embed.title="LOA Coins Discounts & Gifting"
                embed.description="""
Want to give someone else a LOA Coins Product? DM <@!710733052699213844> and tell us who do you want to give it to and we will help you to give them that thing with **NO EXTRA CHARGE**

Discounts available:
- LOA Memberships perks listed above
- 15% off if you own / staff a Lead of Certifications certified server (Refer to ⁠<#941117023914713148> Lead of Certification server)

Note: You **ARE ALLOWED** to use both discounts at the same time
                """


async def setup(bot: Bot) -> None:
    await bot.add_cog(pricelistcog(bot), guild=Object(id=lss))
