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
from assets.buttons import MobileView
from config import hazead, loa
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import LOAWarn, Warn
from typing import List, Optional, Literal


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
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed_embed)
            return

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

                punishment_actions = {
                    3: (
                        "2hr",
                        "2 hour mute punishment applied",
                        "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied",
                    ),
                    6: (
                        None,
                        "Member has reached the 6 warn point punishment. A kick punishment was applied",
                    ),
                    10: (
                        None,
                        "Member has reached the 10 warn point punishment. A ban punishment was applied",
                    ),
                }

                if warnpoints in punishment_actions:
                    action = punishment_actions[warnpoints]
                    if action[0] == "2hr":
                        await member.edit(
                            timed_out_until=(utcnow() + timedelta(hours=2)),
                            reason="2 hour mute punishment applied",
                        )
                        result = action[2]
                        try:
                            timeout_msg = Embed(
                                description=f"You have received a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                            )
                            await member.send(embed=timeout_msg)
                        except:
                            pass
                    elif action[0] is None:
                        if warnpoints == 6:
                            try:
                                kick_msg = Embed(
                                    description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                                )
                                await member.send(embed=kick_msg)
                            except:
                                pass
                            await member.kick(reason="Kick punishment applied")
                        elif warnpoints == 10:
                            try:
                                ban_msg = Embed(
                                    description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                                )
                                ban_msg.set_footer(
                                    text="To appeal for your ban, join with this invite code: qZFhxyhTQh"
                                )
                                await member.send(embed=ban_msg)
                            except:
                                pass
                            await member.kick(reason="Kick punishment applied")
                        result = action[1]
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
        adwarn_channel = await ctx.guild.fetch_channel(745107170827305080)
        if member == ctx.user:
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed_embed)
        else:
            warn_id = randint(0, 100000)
            embed = Embed(
                title="Lead of Advertising - Advertising Warning", color=Color.red()
            )
            embed.description = "<a:warning:1122999390773194772> **You were warned in __Lead of Advertising__, see below for details** <a:warning:1122999390773194772>"
            embed.add_field(
                name="<a:mod:1122999654913691658> Moderator",
                value=ctx.user.mention,
                inline=False,
            )
            embed.add_field(
                name="<a:arrowsRight:1122999872405119166> Location of Infraction:",
                value=channel.mention,
                inline=False,
            )
            embed.add_field(
                name="<a:bell:1122999564299931689> Reason:", value=reason, inline=False
            )
            if notes is not None:
                embed.add_field(
                    name="<a:alert2:1122999727135395851> Moderator's Notes:",
                    value=notes,
                    inline=False,
                )

            warn_data = LOAWarn(member, ctx.user, warn_id)
            if warn_data.give(channel, reason) == False:
                await ctx.followup.send(
                    f"The member was warned recently. Please wait <t:{warn_data.get_time()}:R>"
                )
            else:
                warn_data.give(channel, reason)
                warnpoints = warn_data.get_points()
                embed.add_field(
                    name="<a:arrowsRight:1122999872405119166> Total Infractions:",
                    value=warnpoints,
                    inline=False,
                )
                embed.add_field(name="Warn ID", value=warn_id, inline=False)

                punishment_actions = {
                    6: ("8hr", "Warned 6 times", "An 8 hour timeout will be applied"),
                    7: ("12hr", "Warned 7 times", "A 12 hour timeout will be applied"),
                    8: ("12hr", "Warned 6 times", "A 12 hour timeout will be applied"),
                    9: ("kick", "Warned 9 times", "Kick"),
                    10: ("ban", None, "Ban"),
                }

                if warnpoints in punishment_actions:
                    action = punishment_actions[warnpoints]
                    if action[0] == "ban":
                        do_act = (
                            "No need to take action. The automod for ban has kicked in"
                        )
                        embed.add_field(
                            name="<a:alert:1122999311257583687> Punishment:",
                            value="Ban",
                            inline=False,
                        )
                        warn_data.delete()
                        try:
                            ban_msg = Embed(
                                description=f"You have been banned from **{ctx.guild.name}** because you have reached the 10 warn point punishment.\n\nTo appeal for your ban, please fill in this form https://forms.gle/kpjMC9RMV1QkBY9t6"
                            )
                            await member.send(embed=ban_msg)
                        except:
                            pass
                        await member.ban(reason="Banned for reaching 10 adwarns")
                    elif action[0] == "kick":
                        mobile_act = f"w!kick {member.id} ?r Warned 9 times"
                        do_act = f"The member has a total of {warnpoints} warnings. Please do `{mobile_act}`"
                        embed.add_field(
                            name="<a:alert:1122999311257583687> Punishment:",
                            value="Kick",
                            inline=False,
                        )
                    else:
                        timeout_duration, timeout_reason, result = action
                        mobile_act = f"w!timeout {member.id} {timeout_duration} ?r {timeout_reason}"
                        do_act = f"The member has a total of {warnpoints} warnings. Please do `{mobile_act}`"
                        embed.add_field(
                            name="<a:alert:1122999311257583687> Punishment:",
                            value=result,
                            inline=False,
                        )
                else:
                    do_act = None
                    embed.add_field(
                        name="<a:alert:1122999311257583687> Punishment:",
                        value="No Punishment",
                        inline=False,
                    )
                LOA_ASPECT = self.bot.get_user(710733052699213844)
                embed.set_footer(
                    text="If you feel this warn was a mistake, please use `/appeal apply WARN_ID` or DM {} to appeal".format(
                        LOA_ASPECT
                    )
                )
                embed.set_thumbnail(url=member.display_avatar)
                await adwarn_channel.send(member.mention, embed=embed)
                await ctx.followup.send(
                    f"Warning sent. Check {adwarn_channel.mention}", ephemeral=True
                )

                if do_act:
                    view = MobileView(ctx.user)
                    await ctx.channel.send(
                        "{}\n\n{}".format(ctx.user.mention, do_act), view=view
                    )
                    await view.wait()

                    if view.value:
                        await ctx.edit_original_response(view=None)
                        await ctx.channel.send(
                            embed=Embed(description=mobile_act, color=Color.random())
                        )
                    else:
                        pass

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(
        925790259294396455,
        925790259319558154,
        1011971782426767390,
        980142809094971423,
        972072908065218560,
    )
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
        notes="Add notes if necessary",
    )
    @Serverutil.choices()
    async def adwarn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        await ctx.response.defer()
        if ctx.guild.id == 925790259160166460:
            await self.HA_warn(ctx, member, channel, reason, notes)
        elif ctx.guild.id == 704888699590279221:
            await self.LOA_warn(ctx, member, channel, reason, notes)

    @adwarn.autocomplete("reason")
    async def autocomplete_callback(
        self, ctx: Interaction, current: str
    ) -> List[Serverutil.Choice[str]]:
        if ctx.guild.id == 925790259160166460:
            reasons = [
                "Ad has an invalid invite",
                "Back-to-Back advertising",
                "Ad contains a public ping or mention",
                "Ad is an invite reward server",
                "NSFW ad, imagery or description",
                "Advertising in wrong channel",
                "Ad has a short description",
                "Ad has a long description",
            ]
            return [
                Serverutil.Choice(name=reason, value=reason)
                for reason in reasons
                if current.lower() in reason.lower()
            ]
        elif ctx.guild.id == 704888699590279221:
            reasons = [
                "Ad has an invalid invite",
                "Back-to-Back advertising",
                "Ad contains a public ping or mention",
                "Ad is an invite reward server",
                "NSFW ad, imagery or description",
                "Advertising in wrong channel",
            ]
            return [
                Serverutil.Choice(name=reason, value=reason)
                for reason in reasons
                if current.lower() in reason.lower()
            ]

    @Serverutil.command(description="Remove an adwarn")
    @Serverutil.describe(
        member="Which member recieved the adwarn?",
        warn_id="What is the warn ID you are removing?",
        reason="What was the reason for removing it?",
    )
    @Serverutil.checks.has_any_role(
        925790259319558157,
        889019375988916264,
        947109389855248504,
        961433835277516822,
        919410986249756673,
    )
    async def remove(self, ctx: Interaction, member: Member, warn_id: int, reason: str):
        await ctx.response.defer()
        warn_data = LOAWarn(user=member, warn_id=warn_id)

        if warn_data.check() == None:
            await ctx.followup.send(
                "This user has not been warned or incorrect warn ID",
                ephemeral=True,
            )
        else:
            modchannel1 = await ctx.guild.fetch_channel(954594959074418738)
            if ctx.channel.id == 954594959074418738:
                warn_data.remove()
                modchannel = await ctx.guild.fetch_channel(745107170827305080)
                removed = Embed(
                    description=f"Adwarn with Warn ID `{warn_id}` has been removed. You now have {warn_data.get_points()} adwarns",
                    color=Color.random(),
                )
                removed.add_field(name="Reason", value=reason, inline=False)
                
                await ctx.followup.send("Adwarn Removed")
                await modchannel.send(member.mention, embed=removed)
            else:
                await ctx.followup.send(
                    "Please do this command in {}".format(modchannel1.mention)
                )


async def setup(bot: Bot):
    await bot.add_cog(warncog(bot), guilds=[Object(hazead), Object(loa)])
