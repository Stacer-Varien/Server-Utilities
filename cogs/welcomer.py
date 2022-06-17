from nextcord import *
from nextcord.ext.commands import Cog


WELCOME_CHANNEL_ID = 925790259877412877


class staff(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
            try:
                channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
                try:
                    welcome = f"{member.mention}\n\nHello and welcome to {member.guild.name}!\nBefore you can start advertising and chatting, please read the <#925790259877412876> and <#925790259877412883> so you don't get in trouble. Now please, enjoy your stay and start advertising yourself!\n\n **__Associated Servers:__**\n1. HAZE: https://discord.gg/VVxGUmqQhF\n2. Lead of Advertising: https://discord.gg/gpDcZfF\n**__Special Servers__**\n1. :palm_tree:VIBE WAVE:palm_tree: https://discord.gg/nF8TrX8MEq\n2. Semi-Erasor https://discord.gg/VhgWsfN8ku"

                    embed = Embed(colour=Colour.blue())
                    if member.avatar != None:
                     embed.set_thumbnail(url=member.avatar)
                    else:
                        pass
                    embed.set_image(
                        url="https://media.discordapp.net/attachments/829041410556690452/951799345324376065/swim-ad.gif")
                    await channel.send(welcome, embed=embed)
                except Exception as e:
                    raise e
            except Exception as e:
                raise e

    @Cog.listener()
    async def on_member_remove(self, member):
            try:
                channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
                try:
                    bye = f"{member} left us."
                    await channel.send(bye)
                except Exception as e:
                    raise e
            except Exception as e:
                raise e


def setup(bot):
    bot.add_cog(staff(bot))
