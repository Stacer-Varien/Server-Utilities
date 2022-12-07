from nextcord import *
from nextcord.ext.commands import Cog, Bot

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
                welcome = f"{member.mention}\n\nHello and welcome to {member.guild.name}!\nBefore you can start advertising and chatting, please read the <#925790259877412876> and <#925790259877412883> so you don't get in trouble. Now please, enjoy your stay and start advertising yourself!\n\n **__Special Servers:__**\n1. Lead of Advertising: https://discord.gg/gpDcZfF\n2. Semi-Erasor https://discord.gg/VhgWsfN8ku\n3. Orleans https://discord.gg/Vfa796yvNq"

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
        else:
            pass

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        if member.guild.id == HAZE_ADS:
            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            try:
                bye = f"{member} left us."
                await channel.send(bye)
            except Exception as e:
                raise e

        elif member.guild.id == 841671029066956831:
            channel = self.bot.get_channel(841672222136991757)
            try:
                check_resignation_data = db.execute("SELECT accepted FROM resignData WHERE user_id = ?", (
                member.id,)).fetchone()  # checks for their user ID in the database if it exists

                if check_resignation_data == None:  # if they just left without requesting for resigning
                    no_resign = Embed(title=f"{member} ({member.id}) left the server", color=Color.red())
                    await channel.send(embed=no_resign)

                elif check_resignation_data[0] == 0:  # if they left without an accepted resignation
                    not_accepted = Embed(title=f"{member} ({member.id}) left the server", color=Color.red())
                    await channel.send(embed=not_accepted)

                elif check_resignation_data[0] == 1:  # if their resignation has been accepted and they were kicked out
                    db.execute("DELETE FROM resignData WHERE user_id = ?", (member.id,))
                    db.commit()
                    accepted = Embed(title=f"{member} ({member.id}) has resigned.", color=Color.green())
                    await channel.send(embed=accepted)
            except Exception as e:
                print(e)
        else:
            pass


def setup(bot: Bot):
    bot.add_cog(member(bot))
