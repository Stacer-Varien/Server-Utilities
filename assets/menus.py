from discord import ui, Interaction, SelectOption, Embed, Color


class ProductMenu(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="Shoutout and Custom Channels"),
            SelectOption(label="Giveaways"),
            SelectOption(label="Memberships"),
            SelectOption(label="Special Packages"),
        ]
        super().__init__(
            placeholder="Select an option", max_values=1, min_values=1, options=options
        )

    async def callback(self, ctx: Interaction):
        if self.values[0] == "Shoutout and Custom Channels":
            shouts = Embed(color=Color.blue())
            shouts.title = "Shoutouts & Custom Channels"
            shouts.description = """
Normal Custom Channels ( Without Pings, last for 7 days ) : 800

Add-ons:
- Shoutout Ping : 100
- Partner Ping: 60
- Others Ping: 40
- Real Custom Channel ( You may put anything you want in the channel at anytime, but no more roles will be pinged and the content must fit the <#705956109592035389> ) : 350
- Per day after the first 7 days: 100
- Custom channel emoji: 50**Giveaways**

Normal Shoutout ( Without Pings ) : 400

Add-ons:
- Shoutout Ping : 50
- Partner Ping : 30
- Others Ping: 20**💰LOA Coins Programme Products💰**
"""
            await ctx.response.edit_message(embed=shouts)
        elif self.values[0] == "Giveaways":
            giveads = Embed(color=Color.blue())
            giveads.title = "Giveaways & Auto Advertisements"
            giveads.description = """
Normal Giveaway ( With Giveaway Ping & Requires to join your server, lasts for 1 day ) : 1500

Add-ons:
- Dedicated Channel: 1000
- Prize provided by your server : 0
- Prize in our server : 50 per person
- Each winner (originally one winner) : 10
- Each day (duration of the giveaway, 1 day is given originally) : 10
- No bonus entries allowed (Bonus entries are provided for certain roles): 1000**Shoutouts**
"""
            await ctx.response.edit_message(embed=giveads)
        elif self.values[0] == "Memberships":
            memberships = Embed(color=Color.blue())
            memberships.title = "Memberships"
            memberships.description = """
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

^ = Available in Lead of Advertising and Lead of Gaming**Custom Channels**
Each shoutout is sent with a shoutout ping
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
- Add-ons for pings: the price for shoutouts add-ons * 10

<#959811761282891856> with Job Announcement Ping (No links are allowed) :
- per announcement: 7000
- Default stay for 1 day, after default stay time per day: 3000
- If the content contains nitro emoji the user can post it themself: 300**Memberships**
"""
            await ctx.response.edit_message(embed=special)


class ProductSelect(ui.View):
    def __init__(self):
        super().__init__(timeout=360)
        self.add_item(ProductMenu())
