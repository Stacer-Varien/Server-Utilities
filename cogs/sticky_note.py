from nextcord.ext.commands import Cog
from nextcord.abc import *
from nextcord import *


advertising_channels = [926453405726175232, 926453476408590387, 949733907392253952, 950138528459784334, 950355247530922034, 925790260695281703, 952141249845014569, 951756518192197712, 950137900178210826, 925790260997283851, 925790260997283853, 925790260997283855, 950137942322610206, 925790260997283857, 925790260997283859, 925790261240561714, 925790261240561716, 925790261240561717, 950356056456986624,
                        925790261240561718, 925790261240561719, 925790261240561720, 925790261240561722, 952139192505344021, 925790261240561723, 925790261437669387, 925790261437669390, 926187175282868254, 951385958924828713, 925790261437669392, 930029339137933332, 930029354052894740, 930029368972042261, 930029393156386836, 930029405529575434, 925790260695281698, 925790260695281699, 925790260695281700, 925790260695281701]


class sticky_notecog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if "" in message.content:
            if message.channel.id in advertising_channels:
                if not message.author.bot:
                    msg = Embed(
                        description=f"Thank you for advertising in {message.guild.name}", color=0x1b03a3)

                    msg.add_field(name="Please make sure your ad:",
                                  value="**>** Follows all kinds of ToS\n**>** Follows our advertising and server rules\n**>** Does not contain public pings\n**>** Does not contain NSFW material", inline=False)
                    msg.add_field(name="Want special access and/or more perks?",
                                  value="**>** [Partner with us!](https://discord.com/channels/925790259160166460/925790260263256175/949651798820532275)\n**>** [Make an alliance with us!](https://discord.com/channels/925790259160166460/949750849666687116/949751370632798258)\n**>** [Vote for this server for Premium Role](https://top.gg/servers/925790259160166460)\n**>** Boost the server for special perks")

                    note = await message.channel.send(embed=msg)

                    def check(m):
                        return m.author == message.author and m.content

                    await self.bot.wait_for('message', check=check)
                    await note.delete()
                    await message.channel.send(embed=msg)
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(sticky_notecog(bot))
