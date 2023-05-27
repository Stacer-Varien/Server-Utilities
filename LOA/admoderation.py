from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Message,
    Object,
    TextChannel,
    Forbidden,
    app_commands as Serverutil,
)
from discord.ext.commands import Cog, Bot, GroupCog
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import LOAWarn, LOAMod
from config import lss, loa
import asyncio


class LOAmodCog(GroupCog, name="moderation"):
    def __init__(self, bot: Bot):
        self.bot = bot

    modgroup = Serverutil.Group(name="checks", description="...")

    @modgroup.command(
        name="stats",
        description="Check who has done the most ad moderations for the week",
    )
    @Serverutil.checks.has_role(1075400097615052900)
    async def _stats(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.blue())
        embed.description = await LOAMod().checks(self.bot)
        embed.set_footer(
            text="If a moderator's name is not there, they have not commited an adwarn command."
        )
        await ctx.followup.send(embed=embed)

    @modgroup.command(name="reset", description="Resets last week's checks")
    @Serverutil.checks.has_any_role(
        1074770189582872606,
        1074770253294342144,
        1074770323293085716,
        1076650317392916591,
        949147509660483614,
    )
    async def _reset(self, ctx: Interaction):
        await ctx.response.defer()
        if LOAMod().today <= LOAMod().sunday:
            await ctx.followup.send(
                "DON'T RESET YET!\n\nYou can do a reset on {} to clear the database".format(
                    LOAMod().sunday.strftime("%d-%m-%Y")
                )
            )
        else:
            LOAMod().reset_week()
            await ctx.followup.send("Moderator checks for last week have been reseted")

    @_stats.error
    async def _stats_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.MissingAnyRole):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed)

    @_reset.error
    async def _reset_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.MissingAnyRole):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed)


class LOAwarncog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def warn_message(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
    ):
        adwarn_channel = ctx.guild.get_channel(745107170827305080)
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)
        else:
            embed = Embed()
            warn_id = randint(0, 100000)
            embed = Embed(title="Moderation Record", color=0xFF0000)
            embed.add_field(
                name="Channel of incident occured", value=channel.mention, inline=False
            )
            embed.add_field(name="Moderator", value=ctx.user.mention, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)

            warn_data = LOAWarn(member, ctx.user, warn_id)
            if warn_data.give(channel, reason) == False:
                return await ctx.followup.send(
                    f"The member was warned recently. Please wait after <t:{warn_data.get_time()}:t>"
                )
            else:
                warn_data.give(channel, reason)
                warnpoints = warn_data.get_points()
                embed.add_field(name="Warn ID", value=warn_id, inline=True)
                embed.add_field(name="Warn Points", value=warnpoints, inline=True)

                if warnpoints == 6:
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=8)),
                        reason="8 hour mute punishment applied",
                    )
                    result = "8 hour timeout punishment applied"

                    try:
                        timeoutmsg = Embed(
                            description=f"You have recieved a timeout of 8 hours from **{ctx.guild.name}** because you have reached 6 warn points"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                if warnpoints == 7:
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=12)),
                        reason="12 hour mute punishment applied",
                    )
                    result = "12 hour timeout punishment applied"

                    try:
                        timeoutmsg = Embed(
                            description=f"You have recieved a timeout of 12 hours from **{ctx.guild.name}** because you have reached 7 warn points"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                if warnpoints == 8:
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=12)),
                        reason="24 hour mute punishment applied",
                    )
                    result = "24 hour timeout punishment applied"

                    try:
                        timeoutmsg = Embed(
                            description=f"You have recieved a timeout of 24 hours from **{ctx.guild.name}** because you have reached 8 warn points"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                elif warnpoints == 9:
                    try:
                        kickmsg = Embed(
                            description=f"You are kicked from **{ctx.guild.name}** because you have reached 9 warn points"
                        )
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached 9 warn points. A kick punishment was applied"

                elif warnpoints == 10:
                    try:
                        banmsg = Embed(
                            description=f"You have been banned from **{ctx.guild.name}** bacuse you have reached the 10 warn point punishment.\n\nTo appeal for your ban, please fill in this form https://forms.gle/kpjMC9RMV1QkBY9t6"
                        )
                        await member.send(embed=banmsg)
                    except:
                        pass
                    await member.kick(reason="Ban punishment applied")
                    result = "Member has reached 10 warn points. A ban punishment was applied"

                else:
                    result = "No warn point punishment applied"

                    embed.add_field(name="Result", value=result, inline=False)
                    LOA_ASPECT = self.bot.get_user(710733052699213844)
                    embed.set_footer(
                        text="If you feel this warn was a mistake, please DM {} to appeal or use `/appeal apply WARN_ID".format(
                            LOA_ASPECT
                        )
                    )
                    embed.set_thumbnail(url=member.display_avatar)
                    await adwarn_channel.send(member.mention, embed=embed)
                    await ctx.followup.send(
                        f"Warning sent. Check {adwarn_channel.mention}", ephemeral=True
                    )

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(980142809094971423)
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What was the reason for the warn?",
    )
    async def adwarn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
    ):
        await ctx.response.defer()
        await self.warn_message(ctx, member, channel, reason)

    @Serverutil.command(
        description="Remove someone's warning if it was appealed or given by mistake"
    )
    @Serverutil.checks.has_any_role(
        749608853376598116, 889019375988916264, 1076677389167378432, 947109389855248504
    )
    async def revoke(self, ctx: Interaction, member: Member, warn_id: str):
        await ctx.response.defer()
        data = LOAWarn(member, warn_id=int(warn_id))
        if data.check() == None:
            await ctx.followup.send("Incorrect Warn ID/Member given")
        else:
            adwarn_channel = ctx.guild.get_channel(745107170827305080)
            data.remove()
            embed = Embed(color=Color.random())
            embed.description = (
                "Your warning has been revoked. You now have {} warn points".format(
                    data.get_points()
                )
            )
            await ctx.followup.send("{}'s warn has been removed.".format(member))
            await adwarn_channel.send(member.mention, embed=embed)

    appealgroup = Serverutil.Group(name="appeal", description="...")


class AppealLOA(GroupCog, name="appeal"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def adwarn_appeal(self, ctx: Interaction, warn_id: str):
        warn_data = LOAWarn(user=ctx.user, warn_id=int(warn_id)).check()

        if warn_data is None:
            await ctx.followup.send(
                "You do not have a warning corresponding to this warn ID",
                ephemeral=True,
            )
        else:
            try:
                dm_msg = await ctx.user.send(
                    "Please explain why your adwarn should be revoked? If applicable, please send media content to support your appeal. Please know that sending your ad ONLY would be considered as instant DM advertising and your appeal will be denied.\n\nYou have 5 minutes to appeal"
                )
                await ctx.followup.send(
                    f"[Click here]({dm_msg.jump_url}) to process your appeal"
                )

                def check(m: Message):
                    attachments = bool(m.attachments)
                    content = bool(m.content)
                    if attachments and content:
                        return m.author == ctx.user and m.content and m.attachments
                    elif content:
                        return m.author == ctx.user and m.content
                    elif attachments:
                        return m.author == ctx.user and m.attachments
                    elif attachments and not content:
                        return m.author == ctx.user and m.attachments

                try:
                    appeal_log = await self.bot.fetch_channel(1112136237034246205)
                    msg = await self.bot.wait_for("message", check=check, timeout=600)

                    await ctx.user.send(
                        "Thank you for appealing for your warn. The appropriate staff member will review it and will send updates if any action is needed. Please do not rush us, or your appeal will be denied."
                    )

                    embed = Embed(description="New Warn Appeal", color=Color.random())
                    embed.add_field(
                        name="Person who is appealing it",
                        value=f"{ctx.user} | `{ctx.user.id}`",
                        inline=False,
                    )
                    embed.add_field(name="Warn ID", value=warn_id, inline=False)
                    embed.add_field(
                        name="Reason of warn", value=str(warn_data[1]), inline=False
                    )
                    embed.set_footer(
                        text="To approve or deny this appeal, use `/appeal deny WARN_ID` or `/appeal approve WARN_ID`"
                    )

                    try:
                        image_urls = [x.url for x in msg.attachments]
                        images = "\n".join(image_urls)
                        await appeal_log.send(f"{msg.content}\n{images}", embed=embed)
                    except:
                        await appeal_log.send(msg.content, embed=embed)

                    await ctx.user.send(
                        "Your appeal has been submitted. Please wait patiently for the appropriate staff to decide. Rushing us could increase your chance of your appeal being denied."
                    )
                except asyncio.TimeoutError:
                    await ctx.user.send("Time's up! Please try again later")
            except Forbidden:
                await ctx.followup.send(
                    "Please open your DMs to start the appeal process"
                )

    @Serverutil.command(description="Appeal for your warn if you feel it was a mistake")
    @Serverutil.describe(warn_id="Insert the warn ID you wish to appeal")
    async def apply(self, ctx: Interaction, warn_id: str):
        await ctx.response.defer()
        await self.adwarn_appeal(ctx, warn_id)

    @Serverutil.command(description="Approve an appeal for an adwarn")
    @Serverutil.checks.has_any_role(
        889019375988916264, 947109389855248504, 961433835277516822, 919410986249756673
    )
    async def approve(self, ctx: Interaction, user: Member, warn_id: str):
        await ctx.response.defer()
        warn_data = LOAWarn(user=user, warn_id=int(warn_id))

        if warn_data.check() is None:
            await ctx.followup.send(
                "This user has not been warned or the warn ID is incorrect",
                ephemeral=True,
            )
        else:
            warn_data.remove()
            appeal_channel = await ctx.guild.fetch_channel(1112136237034246205)
            if ctx.channel.id == 1112136237034246205:
                modchannel = await ctx.guild.fetch_channel(745107170827305080)
                appeal_embed = Embed(
                    description=f"Your appeal has been approved. You now have {warn_data.get_points()} adwarns",
                    color=Color.random(),
                )
                await ctx.followup.send("Appeal approved")
                await modchannel.send(user.mention, embed=appeal_embed)
            else:
                await ctx.followup.send(
                    f"Please do this command in {appeal_channel.mention}"
                )


async def setup(bot: Bot):
    await bot.add_cog(LOAmodCog(bot), guild=Object(lss))
    await bot.add_cog(LOAwarncog(bot), guild=Object(loa))
    await bot.add_cog(AppealLOA(bot), guild=Object(loa, lss))
