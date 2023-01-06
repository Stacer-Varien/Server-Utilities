from nextcord import *


class ProductMenu(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="Shoutout and Custom Channels"),
            SelectOption(label="Giveaways and Auto Advertisements"),
            SelectOption(label="Memberships"),
            SelectOption(label="Open Network Auto Advertisement"),
            SelectOption(label="Special Packages")
        ]
        super().__init__(placeholder="Select an option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0] == "Shoutout and Custom Channels":
            shouts = Embed(color=Color.blue())
            shouts.title = "Shoutouts & Custom Channels"
            shouts.description = """
Normal Shoutout ( Without Pings ) : 400

Add-ons:
- Shoutout Ping : 50
- Partner Ping : 30
- Others Ping: 20


Normal Custom Channels ( Without Pings, last for 7 days ) : 800

Add-ons:
- Shoutout Ping : 100
- Partner Ping: 60
- Others Ping: 40
- Real Custom Channel ( You may put anything you want in the channel at anytime, but no more roles will be pinged and the content must fit the <#705956109592035389> ) : 350
- Per day after the first 7 days: 100
"""
            await ctx.response.edit_message(embed=shouts)
        elif self.values[0] == "Giveaways and Auto Advertisements":
            giveads = Embed(color=Color.blue())
            giveads.title = "Giveaways & Auto Advertisements"
            giveads.description = """
Normal Giveaway ( With Giveaway Ping & Requires to join your server, lasts for 1 day ) : 1000

Add-ons:
- Dedicated Channel: 800
- Prize provided by your server : 0
- Prize in our server : 50 per person
- Each winner (originally one winner) : 10
- Each day (duration of the giveaway, 1 day is given originally) : 10

#757476260690657281> : 600
Normal Auto Advertisements ( Every 8 hours ) for 7 days in <

Add-ons:
- Every 4 hours : 100
- Every 2 hours : 200
- Every 30 minutes : 400
- Each channel of your choice : 300
"""
            await ctx.response.send_message(embed=giveads)
        elif self.values[0] == "Memberships":
            memberships = Embed(color=Color.blue())
            memberships.title = "Memberships"
            memberships.description = """
LOA Premium Membership
- 30 days: 3000 LOA Coins
- 365 (a year): 30000 LOA Coins ( ⭐ saving 6000 LOA Coins)

What is included in Premium Membership:
- Premium Role in Lead of Advertising
- Access to <#716897785961775165>
- Monthly Shoutout (DM <@!710733052699213844> to claim at the 1st day of each month)
- Access to VIP Lounge

LOA Executive Membership
- 30 days: 8000 LOA Coins
- 365 (a year): 80000 LOA Cions (⭐ saving 16000 LOA Coins)

What is included in Executive Membership:
- All above perks
- Bonus entries when joining giveaways
- VIP role in all <#941117023914713148> servers (if have^)
- Access to all <#941117023914713148> servers VIP Lounge (if have^)
- 5 shoutouts for free for each month (each shoutout must be claimed after 24 hours of the previous shoutout claiming time)
- 20% off per each <#869201807828725790> purchasement

^ = Available in Lead of Advertising, LOA Safety Centre and Lead of Gaming
"""
            await ctx.response.send_message(embed=memberships)
        elif self.values[0] == "Open Network Auto Advertisement":
            openads = Embed(color=Color.blue())
            openads.title = "Open Network Auto Advertisement"
            openads.description = """
Auto Advertisement for 7 days - 50000

Add-ons:
- Every 4 hours: 0 (default)
- Every 1 hour: 500
- Server advertisement less than 50 characters: 200
- Per day after default: 400 
"""
            await ctx.edit_original_message(embed=openads)
        elif self.values[0] == "Special Packages":
            special = Embed(color=Color.blue())
            special.title = "Special Packages"
            special.description = """
Custom channel under <#707117465049759744> category:
- 1 day: 10000
- per day after that one day: 8000

Custom Channel on the top of the server:
- 1 day: 15000
- per day after that one day: 12500

<#959811761282891856> with Job Announcement Ping:
- per announcement: 5000
- Default stay for 1 day, after default stay time per day: 1000  
"""
            await ctx.edit_original_message(embed=special)


class ProductSelect(ui.View):
    def __init__(self):
        super().__init__(timeout=360)
        self.add_item(ProductMenu())
