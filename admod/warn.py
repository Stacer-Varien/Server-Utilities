from nextcord import slash_command as slash
from nextcord import *
from nextcord.abc import *
from nextcord.ext.commands import Cog
from config import hazead, db
from random import *
from datetime import *
from nextcord.utils import utcnow


class warncog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description="Adwarn someone for violating the ad rules", guild_ids=[hazead])
    async def warn(self, ctx: Interaction, member: Member):
        await ctx.response.defer(ephemeral=True)
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if ctx.permissions.kick_members is True:

                if member == ctx.user:
                        failed = Embed(description="You can't warn yourself")
                        await ctx.followup.send(embed=failed)
                
                else:
                    await ctx.followup.send("Why are they being warned?\nPlease do:\nCHANNEL WERE IT WAS DELETED - REASON per every channel it was deleted\n\nPlease note you have 6 minutes to type")

                    def check(m):
                        return m.author == ctx.user and m.content

                    try:
                        reason=await self.bot.wait_for('message', check=check, timeout=360)


                        warn_id = f"{randint(0,100000)}"
                        appeal_id= f"{randint(0,100000)}"

                        db.execute("INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                                         (member.id, ctx.user.id, reason.content, warn_id, appeal_id))

                        cursor2 = db.execute(
                           "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point) VALUES (?,?)", (member.id, 1))


                        if cursor2.rowcount == 0:
                            db.execute(
                                "UPDATE warnData_v2 SET warn_point = warn_point + 1 WHERE user_id = ?", (member.id,))
                        db.commit()

                        warnpointdata = db.execute(
                                f"SELECT warn_point FROM warnData_v2 WHERE user_id = {member.id}")
                        warn_point = int(warnpointdata.fetchone()[0])


                        embed = Embed(
                            title="You have been warned", color=0xFF0000)
                        embed.add_field(name="Reason for warn", value=reason.content, inline=False)
                        embed.add_field(
                            name="Warn ID", value=warn_id, inline=True)
                        embed.add_field(name="Warn Points", value=warn_point, inline=True)

                        if warn_point == 3:
                            await member.edit(timeout=utcnow()+timedelta(hours=2), reason="2 hour mute punishment applied")
                            result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"

                        elif warn_point == 6:
                            try:
                                kickmsg = Embed(
                                    description=f"You are kicked from **{member.name}**\nYou have reached the 6 warn point punishment")
                                await member.send(embed=kickmsg)
                            except:
                                pass
                            await member.kick(reason="Kick punishment applied")
                            result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                        elif warn_point == 10:
                            try:
                                banmsg = Embed(
                                    description=f"You are banned from **{member.name}**\nYou have reached the 10 warn point punishment")
                                banmsg.set_footer(
                                    text="To appeal for your ban, click [here](https://discord.gg/qZFhxyhTQh)to the ban appeal server")
                                await member.send(embed=kickmsg)
                            except:
                                pass
                            await member.kick(reason="Kick punishment applied")
                            result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                        else:
                            result = 'No warn point punishment applied'

                        embed.add_field(
                            name="Result", value=result, inline=False)
                        embed.set_footer(
                            text="If you feel this warn was a mistake, please use `/appeal WARN_ID`")
                        embed.set_thumbnail(url=member.display_avatar)
                        await adwarn_channel.send(member.mention, embed=embed)
                        await ctx.followup.send(f"Warning sent. Check {adwarn_channel.mention}")
                    except TimeoutError:
                        await ctx.followup.send("Timeout", ephemeral=True)
                    


def setup(bot):
    bot.add_cog(warncog(bot))
