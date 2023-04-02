from discord import app_commands as Serverutil
from discord import *
from discord.abc import *
from discord.ext.commands import Cog, Bot
from config import hazead, loa
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import *
from typing import Optional, Literal


class warncog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Adwarn someone for violating the ad rules"
                        )
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
        custom="Write your own reason (only if you picked custom reason)",
        belongsto=
        "Which channel should the ad go to? (only if you selected wrong channel option)"
    )
    @Serverutil.checks.has_any_role(980142809094971423, 925790259319558154,
                                    925790259319558157)
    async def adwarn(
            self,
            ctx: Interaction,
            member: Member,
            channel: TextChannel,
            reason: Literal['Invite reward server', 'NSFW server',
                            'Ad description involves violating the ToS',
                            'Invalid/Expired Invite', 'Public ping used',
                            'Very little to no description',
                            'Back to back advertising',
                            'Advertising in wrong channel', 'Custom reason'],
            custom: Optional[str] = None,
            belongsto: Optional[TextChannel] = None):
        await ctx.response.defer()
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)
        embed = Embed()
        embed.add_field(name="Ad deleted in", value=channel.mention, inline=False)
        if reason == 'Advertising in wrong channel' and not belongsto:
            await ctx.followup.send(
                "Please include a channel to mention where the ad should be placed next time"
            )
        elif reason == 'Custom reason' and not custom:
            await ctx.followup.send("Please add a custom reason")

        else:
            warn_id = randint(0, 100000)
            appeal_id = randint(0, 100000)
            embed = Embed(title="You have been warned", color=0xFF0000)
            if reason == 'Advertising in wrong channel' and belongsto != None:
                embed.add_field(name="Reason for warn",
                                value=reason,
                                inline=False)
                embed.add_field(name="Belongs to",
                                value=belongsto.mention,
                                inline=False)
            elif reason == 'Custom reason' and custom != None:
                embed.add_field(name="Reason for warn",
                                value=custom,
                                inline=False)
            else:
                embed.add_field(name="Reason for warn",
                                value=reason,
                                inline=False)

            if ctx.guild.id == hazead:
                warn_data = Warn(member, ctx.user, warn_id)
                if warn_data.give_adwarn(channel, reason, appeal_id) == False:
                    return

                if reason == 'Custom reason' and custom != None:
                    warn_data.give_adwarn(channel, custom)
                else:
                    warn_data.give_adwarn(channel, reason)
                warnpoints = warn_data.get_warn_points()
                embed.add_field(name="Warn ID", value=warn_id, inline=True)
                embed.add_field(name="Warn Points",
                                value=warnpoints,
                                inline=True)

                if warnpoints == 3:
                    await member.edit(timed_out_until=(utcnow() + timedelta(hours=2)),
                                      reason="2 hour mute punishment applied")
                    result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"

                    try:
                        timeoutmsg = Embed(
                            description=
                            f"You have recieved a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        return

                elif warnpoints == 6:
                    try:
                        kickmsg = Embed(
                            description=
                            f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                        )
                        await member.send(embed=kickmsg)
                    except:
                        return
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                elif warnpoints == 10:
                    try:
                        banmsg = Embed(
                            description=
                            f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                        )
                        banmsg.set_footer(
                            text=
                            "To appeal for your ban, join with this invite code: qZFhxyhTQh"
                        )
                        await member.send(embed=banmsg)
                    except:
                        return
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                else:
                    result = 'No warn point punishment applied'

                    embed.add_field(name="Result", value=result, inline=False)
                    embed.set_footer(
                        text=
                        "If you feel this warn was a mistake, please use `/appeal WARN_ID`"
                    )
                    embed.set_thumbnail(url=member.display_avatar)
                    await adwarn_channel.send(member.mention, embed=embed)
                    await ctx.followup.send(
                        f"Warning sent. Check {adwarn_channel.mention}",
                        ephemeral=True)
            elif ctx.guild.id == loa:
                if ctx.channel.id == 954594959074418738:
                    warn_data = LOAWarn(member, ctx.user, warn_id)
                    if warn_data.give_adwarn(channel, reason) == False:
                        return

                    warn_data.give_adwarn(channel, reason)
                    warnpoints = warn_data.get_warn_points()
                    embed.add_field(name="Warn ID", value=warn_id, inline=True)
                    embed.add_field(name="Warn Points",
                                    value=warnpoints,
                                    inline=True)


                    if warnpoints <=5:
                        result = "No punishment given"
                    elif warnpoints==6:
                        await member.edit(
                            timed_out_until=(utcnow() + timedelta(hours=6)),
                            reason="6 hour timeout punishment applied")
                        result = "6 hour timeout punishment applied"
                    elif warnpoints == 7:
                        await member.edit(
                            timed_out_until=(utcnow() + timedelta(hours=6)),
                            reason="12 hour timeout punishment applied")
                        result = "12 hour timeout punishment applied"
                    elif warnpoints == 8:
                        await member.edit(
                            timed_out_until=(utcnow() + timedelta(hours=6)),
                            reason="24 hour timeout punishment applied")
                        result = "24 hour timeout punishment applied"
                    elif warnpoints == 9:
                        await member.kick(
                            reason="Reached warn condition for kick")
                        result = "Kick"
                    elif warnpoints == 10:
                        await member.kick(
                            reason="Reached warn condition for ban")
                        result = "Ban"

                    embed.add_field(name="Punishment",
                                    value=result,
                                    inline=False)
                    openmod_channel = await ctx.guild.fetch_channel(
                        745107170827305080)
                    await openmod_channel.send(member.mention, embed=embed)
                    await ctx.followup.send(
                        f"Warning sent. Check {openmod_channel.mention}")
                else:
                    await ctx.followup.send(
                        "Please do the commands in {}".format(
                            ctx.guild.get_channel(954594959074418738).mention), ephemeral=True)

async def setup(bot: Bot):
    await bot.add_cog(warncog(bot), guilds=[Object(hazead), Object(loa)])
