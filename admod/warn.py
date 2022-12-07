from nextcord import slash_command as slash
from nextcord import *
from nextcord.abc import *
from nextcord.ext.commands import Cog, Bot
from config import hazead
from random import *
from datetime import *
from nextcord.utils import utcnow
from nextcord.ext.application_checks import has_guild_permissions
from assets.functions import *


class warncog(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @slash(description="Adwarn someone for violating the ad rules", guild_ids=[hazead])
    @has_guild_permissions(kick_members=True)
    async def warn(self, ctx: Interaction, member: Member, channel:abc.GuildChannel=SlashOption(channel_types=[ChannelType.text], required=True), reason=SlashOption(choices=['NSFW server', 'Invite reward server', 'Server has no description (less than 20 characters)', 'Server violates ToS', 'Advertising in wrong channel', 'Back to back advertising (not waiting for another person to advertise)', 'Custom reason'], required=True), custom=SlashOption(description="Write your own reason (only if you picked custom reason)", required=False), belongsto:abc.GuildChannel=SlashOption(description="Which channel should the ad go to? (only if you selected wrong channel option)", channel_types=[ChannelType.text],required=False)):
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

            if give_adwarn(channel, member.id, ctx.user.id, reason, warn_id, appeal_id)==True:
                
                warnpoints = get_warn_points(member.id)               
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

def setup(bot:Bot):
    bot.add_cog(warncog(bot))
