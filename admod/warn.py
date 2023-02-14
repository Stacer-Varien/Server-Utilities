from discord import app_commands as Serverutil
from discord import *
from discord.abc import *
from discord.ext.commands import Cog, Bot
from config import hazead
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import *
from typing import Optional


class warncog(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.describe(channel="Where was the ad deleted?", reason="What is the reason for the warn?", custom="Write your own reason (only if you picked custom reason)", belongsto="Which channel should the ad go to? (only if you selected wrong channel option)")
    @Serverutil.has_permissions(kick_members=True)
    async def adwarn(self, ctx: Interaction, member: Member, channel:TextChannel, reason:str, custom:Optional[str] =None, belongsto:Optional[TextChannel]=None):
        await ctx.response.defer(ephemeral=True)
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
                        failed = Embed(description="You can't warn yourself")
                        await ctx.followup.send(embed=failed)
                
        else:
            warn_id = f"{randint(0,100000)}"
            appeal_id = f"{randint(0,100000)}"
            embed = Embed(title="You have been warned", color=0xFF0000)
            if reason=='Advertising in wrong channel' and not belongsto:
                await ctx.followup.send("Please include a channel to mention where the ad should be placed next time")
            elif reason=='Advertising in wrong channel' and belongsto!=None:
                embed.add_field(
                    name="Reason for warn", value=reason, inline=False)
                embed.add_field(
                    name="Belongs to", value=belongsto, inline=False)
            elif reason=='Custom reason' and not custom:
                await ctx.followup.send("Please add a custom reason")
            elif reason=='Custom reason' and custom!=None:
                embed.add_field(
                    name="Reason for warn", value=custom, inline=False)
            else:
                embed.add_field(
                    name="Reason for warn", value=reason, inline=False)
            
            warn_data = Warn(member, ctx.user, warn_id)
            if warn_data.give_adwarn(channel, reason, appeal_id)==False:
                pass
            else:
                warn_data.give_adwarn(channel, member.id, ctx.user.id,
                            reason, warn_id, appeal_id)
                warnpoints = warn_data.get_warn_points()               
                embed.add_field(
                            name="Warn ID", value=warn_id, inline=True)
                embed.add_field(name="Warn Points", value=warnpoints, inline=True)

                if warnpoints == 3:
                    await member.edit(timeout=utcnow()+timedelta(hours=2), reason="2 hour mute punishment applied")
                    result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"

                    try:
                        timeoutmsg=Embed(
                                    description=f"You have recieved a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment")
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                elif warnpoints == 6:
                    try:
                        kickmsg = Embed(
                                    description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment")
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                elif warnpoints == 10:
                    try:
                        banmsg = Embed(
                            description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment")
                        banmsg.set_footer(
                            text="To appeal for your ban, join with this invite code: qZFhxyhTQh")
                        await member.send(embed=banmsg)
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
                    await ctx.followup.send(f"Warning sent. Check {adwarn_channel.mention}",ephemeral=True)

async def setup(bot:Bot):
    await bot.add_cog(warncog(bot), guild=Object(hazead))
