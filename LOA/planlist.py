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
        await ctx.response.defer(ephemeral=True)
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)

        if ctx.channel.id in thread_cat.channels or ctx.channel.id == 707209752396038215:
                view = ProductSelect()
                embed = Embed()
                embed.color = Color.blue()
                embed.description = "Use the dropmenu below to view a package\nOnce payment is transacted, no refunds will be available."
                await ctx.followup.send(embed=embed, view=view, ephemeral=True)
        else:
            await ctx.followup.send("Please use this command in the appropriate channels", ephemeral=True)
            

    @Serverutil.command(description="Get a list of LOA coin pricelist")
    async def paidplans(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)

        if ctx.channel.id in thread_cat.channels or ctx.channel.id == 707209752396038215:
                embed = Embed(color=Color.blue())
                embed.title = "Paid plans"
                embed.description = """
❗Note:
The below prices are listed in US Dollar 💵 and for the payment method, we currently accept <:nitro:773087831680745482> Nitro Gifts only. Your server must be Safe For Work. We reserve the rights to not accepting you buying the products. We do not guarantee any joins. But this can probably be a good way for letting more people to know about your server. You must pay first. You will also get a high up 💰Buyers role after you have bought a plan! No refund. The prices are just telling you that how much it worths, while most of the time, I can offer discounts
The LOA Sales Terms are attached.
**NEW $3 Nitro Basic Plan:**
- 30 days of Premium Membership
- Custom Channel for 7 days with Shoutout Ping + Partner Ping

or
- 5 days of Embed Message Banner Position

$10 Nitro normal plan:
- Giveaway with prize provided by us (or by your side if you are willing to), 7 days
- Custom Channel with Shoutout Ping + Partner Ping for 30 days
- 10000 LOA Coins
- Premium Role for a month

If you want (Any types of nitro):
- Fully customisable package base on your server type and size
What you can get for getting any of our plans:
- ⭐ Shiny high up <@&816242764621676586> role
- 🌟 Giveaway bonus entries
<@&816242764621676586> Privileges:

- Access to <#1034985343268683827> right under <#707200066292809808> !!!
- Discounts on extension of plans !!!

Buyers role maintain until the end of the plan
"""
        else:
            await ctx.followup.send("Please use this command in the appropriate channels", ephemeral=True)

    @Serverutil.command(description="Get a list of LOA booster plans")
    async def boosts(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)

        if ctx.channel.id in thread_cat.channels or ctx.channel.id == 707209752396038215:
                embed = Embed(color=Color.blue())
                embed.title = "Booster plans"
                embed.description = """
**Booster Perks**

♦️1 Boost
- Premium Membership for 30 Days (It will be extended if you extend your boosts)
The Membership includes:
> - Premium Role in Lead of Advertising
> - Access to <#716897785961775165>
> - Monthly Shoutout (DM <@710733052699213844> to claim at the 1st day of each month)
> - Access to VIP Lounge
> - Extra Daily LOA Coins
- Shoutout with Shoutout Ping + Partner Ping
- LOA Booster role
- Massive thank you
- Giveaway bonus entries
- 5000 LOA Coins
- Access to <#792539615474090054>
- Free Custom Channel in Spotlight Category
- Your name shown in <#833971349865103360> 

♦️♦️ 2 Boosts

- All above perks
- Additional 8000 LOA Coins
- Custom Channel at the top of the server
- Executive Membership for 30 days (It will be extended if you extend your boosts)
The Membership includes:
> - All Premium Membership Perks
> - Bonus entries when joining giveaways
> - VIP role in all <#941117023914713148> servers (if have^)
> - Access to all <#941117023914713148> servers VIP Lounge (if have^)
> - 5 shoutouts for free for each month (each shoutout must be claimed after 24 hours of the previous shoutout claiming time)
> - 20% off per each <#869201807828725790> purchasement
> - More extra daily LOA Coins
- Legendary Booster Role

♦️ ♦️ ♦️ 3 boosts (if more than 3 boosts please directly dm <@1033533294840664074> for special extra perks)
-All above perks
- Additional 12000 LOA Coins

Perks may changed unannounced. The LOA Group shall not be held liable for any damages cost and shall not be responsible for providing compensation of any sort.

**LOA Coins can be used to purchase products in <#869201807828725790> **

**Register for LOA Coins in <#707209752396038215> with `/registercoins`**
"""
                await ctx.followup.send(embed=embed, ephemeral=True)
        else:
            await ctx.followup.send("Please use this command in the appropriate channels", ephemeral=True)                

async def setup(bot: Bot) -> None:
    await bot.add_cog(pricelistcog(bot), guild=Object(id=lss))
