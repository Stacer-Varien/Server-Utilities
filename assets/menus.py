from discord import ui, Interaction, SelectOption, Embed, Color

class ProductMenu(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="Shoutout and Custom Channels"),
            SelectOption(label="Giveaways"),
            SelectOption(label="Memberships"),
            SelectOption(label="Special Packages"),
            SelectOption(label="LOA Coins Discounts & Gifting")
        ]
        super().__init__(
            placeholder="Select an option", max_values=1, min_values=1, options=options
        )

    async def callback(self, ctx: Interaction):
        if self.values[0] == "Shoutout and Custom Channels":
            shouts = Embed(color=Color.blue())
            shouts.title = "Shoutouts & Custom Channels"
            shouts.description = """
**Shoutouts**
Normal Shoutout ( Without Pings ) : 400

Add-ons:
- Shoutout Ping : 50
- Partner Ping : 30
- Others Ping: 20

Get it with the command `/shop shoutout`! Run it in <#707209752396038215>

**Custom Channels**
Normal Custom Channels ( Without Pings, per day) : 100

Add-ons:
- Shoutout Ping : 60
- Partner Ping: 40
- Others Ping: 20
- Custom channel emoji: 100
- Ping on join: 5000 per day

Get it with the command `/shop customchannel`! Run it in <#707209752396038215>
"""
            await ctx.response.edit_message(embed=shouts)
        elif self.values[0] == "Giveaways":
            giveads = Embed(color=Color.blue())
            giveads.title = "Giveaways"
            giveads.description = """
Normal Giveaway ( With Giveaway Ping & Requires to join your server, lasts for 1 day ) : 1500

Add-ons:
- Dedicated Channel: 1000
- Prize provided by your server : 0
- Prize in our server : 50 per person
- Each winner (originally one winner) : 10
- Each day (duration of the giveaway, 1 day is given originally) : 10
- No bonus entries allowed (Bonus entries are provided for certain roles): 1000
"""
            await ctx.response.edit_message(embed=giveads)
        elif self.values[0] == "Memberships":
            memberships = Embed(color=Color.blue())
            memberships.title = "Memberships"
            memberships.description = """
**__LOA Premium Membership__**
- 30 days: 3000 LOA Coins
- 365 (a year): 30000 LOA Coins ( ⭐ saving 6000 LOA Coins)

What is included in Premium Membership:
- Premium Role in Lead of Advertising
- Access to <#716897785961775165>
- Monthly Shoutout (DM <@710733052699213844> to claim at the 1st day of each month)
- Access to VIP Lounge
- Extra Daily LOA Coins

**__LOA Executive Membership__**
- 30 days: 8000 LOA Coins ( 🪙 Enjoy a special 2000 LOA Coins discount for each renewal!)
- 365 (a year): 80000 LOA Cions (⭐ saving 16000 LOA Coins)

What is included in Executive Membership:
- All above perks
- Bonus entries when joining giveaways
- VIP role in all <#941117023914713148> servers (if have^)
- Access to all <#941117023914713148> servers VIP Lounge (if have^)
- 5 shoutouts for free for each month (each shoutout must be claimed after 24 hours of the previous shoutout claiming time)
- 20% off per each <#869201807828725790> purchasement
- More extra daily LOA Coins

^ = Available in Lead of Advertising and Lead of Gaming
"""
            await ctx.response.edit_message(embed=memberships)
        elif self.values[0] == "Special Packages":
            special = Embed(color=Color.blue())
            special.title = "Special Packages"
            special.description = """
Custom channel under 🎈・General・🎈 category:
- 1 day: 12000
- per day after that one day: 10000

Custom Channel on the top area of the server:
- 1 day: 15000
- per day after that one day: 12500
- Custom emoji: 100 per day
- Add-ons for pings: the price for shoutouts add-ons * 10 per day

<#959811761282891856> with Job Announcement Ping (No links are allowed) :
- per announcement: 7000
- Default stay for 1 day, after default stay time per day: 3000
- If the content contains nitro emoji the user can post it themself: 300
"""
            await ctx.response.edit_message(embed=special)
        elif self.values[0] == "LOA Coins Discounts & Gifting":
            discounts = Embed(color=Color.blue())
            discounts.title = "LOA Coins Discounts & Gifting"
            discounts.description = """
Want to give someone else a LOA Coins Product? DM <@710733052699213844> and tell us who do you want to give it to and we will help you to give them that thing with **NO EXTRA CHARGE**

or

Use `/transfer` command with 2% charge

Discounts available:
- LOA Memberships perks listed above
- 15% off if you own / staff a Lead of Certifications certified server (Refer to <#941117023914713148> Lead of Certification server)

Note: Certified Server Discount is the only discount that allows you to use it with **one** another discount that you have, i.e. Internal Staff Discount / Membership Discount / Discounts issue
"""
            await ctx.response.edit_message(embed=discounts)        


class ProductSelect(ui.View):
    def __init__(self):
        super().__init__(timeout=360)
        self.add_item(ProductMenu())
