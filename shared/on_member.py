from discord import *
from discord.ext.commands import Cog, Bot
from assets.functions import Resign

from config import db

WELCOME_CHANNEL_ID = 925790259877412877
HAZE_ADS = 925790259160166460


class member(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == HAZE_ADS:
            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            try:
                welcome = f"{member.mention}\n\nHello and welcome to {member.guild.name}!\nBefore you can start advertising and chatting, please read the <#925790259877412876> and <#925790259877412883> so you don't get in trouble. Now please, enjoy your stay and start advertising yourself!\n\n **__Special Servers:__**\n1. Lead of Advertising: https://discord.gg/gpDcZfF\n2. Semi-Erasor https://discord.gg/VhgWsfN8ku\n3. Orleans https://discord.gg/Vfa796yvNq\n4. Safe Space https://discord.gg/HXQFSfZfws"

                embed = Embed(colour=Colour.blue())
                if member.avatar != None:
                    embed.set_thumbnail(url=member.avatar)
                else:
                    pass
                embed.set_image(
                    url=
                    "https://media.discordapp.net/attachments/829041410556690452/951799345324376065/swim-ad.gif"
                )
                await channel.send(welcome, embed=embed)
            except Exception as e:
                raise e
        else:
            pass

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        if member.guild.id == HAZE_ADS:
            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            try:
                bye = f"{member} left us."
                await channel.send(bye)
            except:
                pass

        elif member.guild.id == 841671029066956831:
            channel = self.bot.get_channel(841672222136991757)
            try:
                await Resign(member).resigned(channel)
            except:
                pass



async def setup(bot: Bot):
    await bot.add_cog(member(bot))
