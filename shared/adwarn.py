from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Object,
    TextChannel,
    app_commands as Serverutil,
)
from discord.ext.commands import Cog, Bot
from config import hazead, loa
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import LOAWarn, Warn
from typing import Optional, Literal


class warncog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def HA_warn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)

        else:
            
            embed = Embed()
            warn_id = randint(0, 100000)
            embed = Embed(title="You were adwarned", color=0xFF0000)
            embed.add_field(name="Ad deleted in", value=channel.mention, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            if notes is not None:
                embed.add_field(name="Notes", value=notes, inline=False)

            warn_data = Warn(member, ctx.user, warn_id)
            if warn_data.give(channel, reason) == False:
                await ctx.followup.send(
                    f"Please wait <t:{warn_data.get_time()}:R> to adwarn the member"
                )
            else:
                warn_data.give(channel, reason)
                warnpoints = warn_data.get_points()
                embed.add_field(name="Warn ID", value=warn_id, inline=True)
                embed.add_field(name="Warn Points", value=warnpoints, inline=True)

                if warnpoints == 3:
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=2)),
                        reason="2 hour mute punishment applied",
                    )
                    result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"

                    try:
                        timeoutmsg = Embed(
                            description=f"You have recieved a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                elif warnpoints == 6:
                    try:
                        kickmsg = Embed(
                            description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                        )
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                elif warnpoints == 10:
                    try:
                        banmsg = Embed(
                            description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                        )
                        banmsg.set_footer(
                            text="To appeal for your ban, join with this invite code: qZFhxyhTQh"
                        )
                        await member.send(embed=banmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                else:
                    result = "No warn point punishment applied"

                    embed.add_field(name="Result", value=result, inline=False)
                    embed.set_footer(
                        text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
                    )
                    embed.set_thumbnail(url=member.display_avatar)
                    await adwarn_channel.send(member.mention, embed=embed)
                    await ctx.followup.send(
                        f"Warning sent. Check {adwarn_channel.mention}", ephemeral=True
                    )

    async def LOA_warn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        adwarn_channel = ctx.guild.get_channel(745107170827305080)
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)
            return
        
        warn_id = randint(0, 100000)
        embed = Embed(title="Lead of Advertising - Advertising Warning", color=Color.red())
        embed.description="<a:Caution:1114028164323213383> **You were warned in __Lead of Advertising__, see below for details** <a:Caution:1114028164323213383>"
        embed.add_field(name="Moderator", value=ctx.user.mention, inline=False)
        embed.add_field(
            name="<a:RightArrow:1113978087680528459> Location of Infraction:", value=channel.mention, inline=False
        )
        embed.add_field(name="<a:Bell:1116210304901185698> Reason:", value=reason, inline=False)
        if notes is not None:
            embed.add_field(name="<a:Moderation:1113978137471098992> Moderator's Notes:", value=notes, inline=False)

        warn_data = LOAWarn(member, ctx.user, warn_id)
        if not warn_data.give(channel, reason):
            return await ctx.followup.send(
                f"The member was warned recently. Please wait <t:{warn_data.get_time()}:R>"
            )

        warn_data.give(channel, reason)
        warnpoints = warn_data.get_points()
        embed.add_field(name="<a:Loading2:1116210852920557578> Total Infractions:", value=warnpoints, inline=False)
        embed.add_field(name="Warn ID", value=warn_id, inline=False)

        
        timeout_dict = {
            6: (8, "8 hour timeout"),
            7: (12, "12 hour timeout"),
            8: (12, "24 hour timeout"),
            9: (None, "Kick"),
            10: (None, "Ban"),
        }

        if warnpoints in timeout_dict:
            timeout_hours, result = timeout_dict[warnpoints]

            if timeout_hours is not None:
                await member.edit(
                    timed_out_until=(utcnow() + timedelta(hours=int(timeout_hours))),
                    reason=result,
                )

                try:
                    timeoutmsg = Embed(
                        description=f"You have received a timeout of {timeout_hours} hours from **{ctx.guild.name}** because you have reached {warnpoints} warn points"
                    )
                    await member.send(embed=timeoutmsg)
                except:
                    pass
            else:
                try:
                    if warnpoints == 9:
                        kickmsg = Embed(
                            description=f"You are kicked from **{ctx.guild.name}** because you have reached 9 warn points"
                        )
                        await member.send(embed=kickmsg)
                    elif warnpoints == 10:
                        banmsg = Embed(
                            description=f"You have been banned from **{ctx.guild.name}** because you have reached the 10 warn point punishment.\n\nTo appeal for your ban, please fill in this form https://forms.gle/kpjMC9RMV1QkBY9t6"
                        )
                        await member.send(embed=banmsg)
                except:
                    pass

                if warnpoints == 9:
                    await member.kick(reason="Kicked for reaching 9 adwarns")
                elif warnpoints == 10:
                    await member.ban(reason="Banned for reaching 10 adwarns")

            result = result if warnpoints >= 9 else "No Punishment"
            embed.add_field(name="<a:Timer:1116210678030663740> Punishment:", value=result, inline=False)
            LOA_ASPECT = self.bot.get_user(710733052699213844)
            embed.set_footer(
                text="If you feel this warn was a mistake, please DM {} to appeal".format(
                    LOA_ASPECT
                )
            )
            embed.set_thumbnail(url=member.display_avatar)
            await adwarn_channel.send(member.mention, embed=embed)
            await ctx.followup.send(
                f"Warning sent. Check {adwarn_channel.mention}", ephemeral=True
            )

    async def adwarn_give(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        if ctx.guild.id == 925790259160166460:
            await self.HA_warn(ctx, member, channel, reason, notes)
        elif ctx.guild.id == 704888699590279221:
            await self.LOA_warn(ctx, member, channel, reason, notes)

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(
        925790259294396455, 925790259319558154, 1011971782426767390, 980142809094971423
    )
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
        notes="Add notes if necessary",
    )
    async def adwarn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: Literal[
            "Ad has an invalid invite",
            "Back-to-Back advertising",
            "Ad has a long description",
            "Ad description is too short",
            "Ad is an invite reward server",
            "NSFW ad, imagery or description",
            "Advertising in wrong channel",
        ],
        notes: Optional[str] = None,
    ):
        await ctx.response.defer()
        await self.adwarn_give(ctx, member, channel, reason, notes)


async def setup(bot: Bot):
    await bot.add_cog(warncog(bot), guilds=[Object(hazead), Object(loa)])
