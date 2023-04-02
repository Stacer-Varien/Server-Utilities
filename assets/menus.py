from discord import ui, Interaction, SelectOption, Embed, Color


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
                         max_values=1,
                         min_values=1,
                         options=options)

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
            await ctx.edit_original_response(embed=shouts)
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

Normal Auto Advertisements ( Every 8 hours ) for 7 days in <#757476260690657281> : 600

Add-ons:
- Every 4 hours : 100
- Every 2 hours : 200
- Every 30 minutes : 400
- Each channel of your choice : 300
"""
            await ctx.edit_original_response(embed=giveads)
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
The shoutouts are sent with shoutout ping
"""
            await ctx.edit_original_response(embed=memberships)
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
            await ctx.edit_original_response(embed=openads)
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
            await ctx.edit_original_response(embed=special)


class ProductSelect(ui.View):

    def __init__(self):
        super().__init__(timeout=360)
        self.add_item(ProductMenu())


class PrivacyMenu(ui.Select):

    def __init__(self):
        options = [
            SelectOption(label="Orleans"),
            SelectOption(label="HAZE Advertising"),
            SelectOption(label="Varien's Homework Folder"),
            SelectOption(label="LOA and LSS")
        ]
        super().__init__(placeholder="Select a server",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, ctx: Interaction):
        embed=Embed()
        embed.color=Color.random()
        if self.values[0]=='Orleans':
            embed.title="Privacy Policy effecting Orleans"
            embed.add_field(name="Privacy Policy", value="N/A", inline=False)
            embed.add_field(name="Functions", value="The channel, <#1041309643449827360> is checked for media content and prohibits members to chat in that channel by deleting that message. If a media content has a message content, the bot will allow it.", inline=False)
            await ctx.edit_original_response(embed=embed)
        elif self.values[0] == 'HAZE Advertising':
            embed.title = "Privacy Policy effecting HAZE Advertising"
            embed.add_field(name="Privacy Policy", value="""
Storing and Access of Data
Data such as adwarns and plans are stored in the database. Plans can be viewed to authorised personnel while adwarn data is controlled as the basic data is viewed to everyone while the true data is viewed by the developer.

Removal of Data
Data can be removed if a member's adwarn appeal has been approved and a plan has ended from the database.
            """, inline=False)
            embed.add_field(
                name="Functions",
                value=
                """
1. In non-advertising channels, if the message contains a public ping, the message with that ping gets deleted and the author is automatically adwarned.

2. Members can get automatically punished by the bot if they have reached a condition depending on how many adwarns they have""",
                inline=False)
            await ctx.edit_original_response(embed=embed)
        elif self.values[0] == "Varien's Homework Folder":
            embed.title = "Privacy Policy effecting Varien's Homework Folder"
            embed.add_field(name="Privacy Policy",
                            value="""
Storing of Data
Members that have the 'Untrusted' role in the server are automatically logged into the database with the 48 hour limit. Only the 'Untrusted' data is stored in the database and is not public for everyone to view.

Removal of Data
Members that have the 'Verified' role are automatically removed from the database.
            """,
                            inline=False)
            embed.add_field(name="Functions",
                            value="""
1. In the non-main NSFW channels, the bot deletes a message if it has more than 5 media contents

2. If a member has the 'Untrusted' role, the bot logs it and waits 48 hours for the member to verify. If the member has failed to verify, they are automatically banned""",
                            inline=False)
            await ctx.edit_original_response(embed=embed)

        elif self.values[0] == 'LOA and LSS':
            embed.title = "Privacy Policy effecting LOA and LSS"
            embed.add_field(name="Privacy Policy",
                            value="""
Storing of Data
Data such as adwarns, breaks, resignations, plans and strikes are stored in the database. Adwarns and strikes are controlled as the basic data is viewed by everyone while the true data is viewed by the developer. Resignations and plans can only be viewed by authorised personnel.

Removal of Data
Data is removed if an adwarn has been cleared, breaks approved or denied, end of plans, cleared strike and/or approved or denied resignation.
            """,
                            inline=False)
            embed.add_field(name="Functions",
                            value="N/A",
                            inline=False)
            await ctx.edit_original_response(embed=embed)


class PrivacySelect(ui.View):

    def __init__(self):
        super().__init__(timeout=360)
        self.add_item(PrivacyMenu())