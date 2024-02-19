from discord import Embed, Colour, Member
from discord.ext.commands import Cog, Bot
import asyncio

asyncio.sleep(1)

WELCOME_CHANNEL_ID = 925790259877412877
HAZE_ADS = 925790259160166460


class MemberCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == HAZE_ADS:
            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            welcome = (
                f"{member.mention}\n\nHello and welcome to {member.guild.name}!\n"
                "Before you can start advertising and chatting, please read the "
                "<#925790259877412876> and <#925790259877412883> so you don't get in trouble."
                " Now please, enjoy your stay and start advertising yourself!\n\n"
                " **__Special Servers:__**\n"
                "1. Orleans https://discord.gg/Vfa796yvNq\n"
                "2. Gremory Castle https://rias.gg/discord\n"
                "3. jeanne https://discord.gg/jeanne"
            )

            embed = Embed(colour=Colour.blue())

            embed.set_thumbnail(url=member.display_avatar)

            try:
                await channel.send(welcome, embed=embed)
            except Exception as e:
                print(f"Failed to send welcome message: {e}")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            if member.guild.id == HAZE_ADS:
                channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
                bye = f"{member} left us."
                try:
                    await channel.send(bye)
                except Exception as e:
                    print(f"Failed to send goodbye message: {e}")
        except Exception as e:
            print(f"Error: {e}")


async def setup(bot: Bot):
    await bot.add_cog(MemberCog(bot))
