from nextcord import slash_command as slash, Embed, Interaction
from nextcord.ext.commands import Cog
from config import varien, hazead


class srules(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(guild_ids=[hazead])
    async def rules(self, interaction: Interaction):
        if interaction.user == self.bot.get_user(varien):
            rules = Embed(
                description='Before you can advertise, follow these rules:')
            rules.add_field(name="**1. PLEASE FOLLOW DISCORD'S TOS**",
                            value="If you are not following ToS or previously broke ToS, serious actions will be taken. [Click here to read Discord's ToS](https://discord.com/terms) ", inline=False)
            rules.add_field(name="**2. NO UNWANTED CONTENT OR ADS ALLOWED**",
                            value="This means no NSFW based servers and no NSFW/NSFL content", inline=False)
            rules.add_field(name="**3. NO SPAMMING**",
                            value="Do not spam or send copypastas here or we will mute you", inline=False)
            rules.add_field(name="**4. NO UNNECESSARY PINGING**",
                            value="Only ping if its important. Pinging people or roles for fun will have serious actions taken", inline=False)
            rules.add_field(name="**5. NO SELF PROMO OR MARKETING**",
                            value="We do not allow any kind of DM advertising or self marketing without permission from the member. If we do get a report that you are DM advertising or self marketing, we will ban you with no appeals", inline=False)
            rules.add_field(name="**6. PLEASE HAVE A DECENT USERNAME AND AVATAR**",
                            value="That means no NSFW/NSFL avatars, racist words in usernames/nicknames. Ignoring that rule will have you kicked out", inline=False)
            rules.add_field(name="**7. RESPECT EVERYONE AND BE APPROPRIATE TOWARDS THEM**",
                            value="It means that you should respect everyone and approach them appropriately. That includes everyone that have a life outside Discord.", inline=False)
            rules.add_field(name="**8. READ THE CHANNEL TOPICS**",
                            value="Even if there is some rules not listed here, there are rules put in the channel topics. Failing to abide them is punishable.", inline=False)
            rules.add_field(name="**9. DECISIONS MADE BY ADMINS OR MODS ARE FINAL**",
                            value="Decisions made by admins and mods are final! Picking a fight with them is punishable.", inline=False)
            rules.add_field(name="**10. DO NOT ADVERTISE NSFW LEAKS/INVITE REWARD SERVERS**",
                            value="Advertising them is a bannable punishment", inline=False)
            await interaction.response.send_message(embed=rules)

    @slash(guild_ids=[hazead])
    async def how_to_ad(self, interaction: Interaction):
        disads = self.bot.get_channel(925790260695281702)
        medads = self.bot.get_channel(930019342505099274)
        if interaction.user == self.bot.get_user(varien):
            howad = Embed(description="This will help you how to advertise")
            howad.add_field(name=f"{disads.name}", value="All channels in that section require only Discord ads and nothing else. Make sure the server you are advertising fits the tag. As for Level channels, Time channels and <#925790261240561717>, you can advertise anything (only Discord servers). All ads and servers must be SFW as we do not allow NSFW ads and servers. Please also do", inline=False)
            howad.add_field(name=f"{medads.name}", value="You can post media links in there but <#930029415465877545> is a place for ads you can post if it doesn't meet the required tags. All ads must be SFW as we do not allow NSFW ads", inline=False)
            howad.add_field(name="Do not include any public pings on your ads",
                            value="If you do, it will fail and you will be warned", inline=False)
            howad.add_field(name="Ignoring verbal warnings can lead to serious actions",
                            value="Ignoring the verbal warnings:\n-> 3 times will result in a 2hr mute\n-> 6 times will result in a kick\n-> 10 times will result in a ban. You can appeal [here](https://discord.gg/qZFhxyhTQh) ", inline=False)
            howad.add_field(name="Breaks the ad rules or ToS",
                            value="Posting any ad that breaks the rules or violates ToS (such as advertising an NSFW based server or a server allowing 12 years or younger) will result in all of your ads deleted", inline=False)
            howad.set_footer(
                text="IMPORTANT: Do not advertise in the <#925790260263256180> section. You will be warned for it!")
            await interaction.response.send_message(embed=howad)


def setup(bot):
    bot.add_cog(srules(bot))
