from discord import Embed, Colour, Member
from discord.ext.commands import Cog, Bot


WELCOME_CHANNEL_ID = 925790259877412877
OAD = 925790259160166460


class MemberCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == OAD:
            channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            welcome = (
                f"{member.mention}\n\nHello and welcome to {member.guild.name}!\n"
                "Before you can start advertising and chatting, please read the "
                "<#925790259877412876> and <#925790259877412883> so you don't get in trouble."
                " Now please, enjoy your stay and start advertising yourself!"
            )

            embed = Embed(colour=Colour.blue())

            embed.set_thumbnail(description=welcome, url=member.display_avatar)

            try:
                await channel.send(welcome, embed=embed)
            except Exception as e:
                print(f"Failed to send welcome message: {e}")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            if member.guild.id == OAD:
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
