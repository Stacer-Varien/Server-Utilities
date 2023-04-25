from datetime import datetime, timedelta
from random import randint
from assets.menus import ProductSelect
from humanfriendly import parse_timespan
from discord import Embed, Color, Interaction, Member, CategoryChannel, Object
from discord import app_commands as Serverutil
from discord.ext.commands import Bot, GroupCog, Cog
from assets.functions import Break, LOAWarn, Resign, Strike
from assets.strike_modal import Strike_Appeal
from typing import Literal, Optional
from config import lss, loa

ha_admin = 925790259319558157
ha_hr = 925790259319558156
ha_mod = 925790259319558154
core_team = 841671779394781225  # both
coo = 955722820464283658  # strike + resign
chr = 949147158572056636  # strike + resign
team_leader = 841682891599773767  # strike
staff_supervisor = 962628294627438682  # strike
om = 841671956999045141  # break


class breakcog(GroupCog, name="break"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Apply for break")
    @Serverutil.describe(
        duration_type="Is it timed or until further notice?",
        reason="Why do you want to go on break?",
        duration="If you have selected the timed option, how long are you planning to take break?",
    )
    async def apply(
        self,
        ctx: Interaction,
        duration_type: Literal["Timed (1h, 1h30m, etc)", "Until further notice"],
        reason: str,
        duration: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        break_role = ctx.guild.get_role(841682795277713498)
        channel = await self.bot.fetch_channel(841676953613631499)

        if break_role in ctx.user.roles:
            await ctx.followup.send("You are already on break")
        else:
            if duration_type == "Timed (1h, 1h30m, etc)" and duration == None:
                await ctx.followup.send("You are missing the `duration` option")
            elif duration_type == "Until further notice" and duration != None:
                await ctx.followup.send(
                    "You cannot use the `duration` option if you are going away until further notice"
                )
            else:
                if ctx.user.id == 533792698331824138:
                    break_log = await self.bot.fetch_channel(1001053890277556235)

                    if duration_type == "Until further notice":
                        duration = "Until further notice"
                        Break(ctx.user).add_break_request(
                            ctx.guild.id,
                            duration,
                            reason,
                            1,
                            round(datetime.now().timestamp()),
                            99999999999,
                        )

                    elif duration_type == "Timed (1h, 1h30m, etc)":
                        time = round(
                            (
                                datetime.now()
                                + timedelta(seconds=parse_timespan(duration))
                            ).timestamp()
                        )
                        duration = "<t:{}:D>".format(time)
                        Break(ctx.user).add_break_request(
                            ctx.guild.id,
                            duration,
                            reason,
                            1,
                            round(datetime.now().timestamp()),
                            time,
                        )

                    own_break = Embed(
                        description="You are now on break", color=Color.blue()
                    )
                    own_break.add_field(name="Duration", value=duration, inline=False)

                    await ctx.user.add_roles(break_role, reason="Owner on break")
                    await channel.send(ctx.user.mention, embed=own_break)

                    auto_break = Embed(title="Break Automatically Given")
                    auto_break.add_field(
                        name="Staff Member", value=ctx.user, inline=False
                    )
                    auto_break.add_field(
                        name="Role", value=ctx.user.top_role, inline=False
                    )
                    auto_break.add_field(name="Duration", value=duration, inline=False)
                    auto_break.add_field(name="Reason", value=reason, inline=False)

                    await break_log.send(embed=auto_break)

                else:
                    requested_break = Embed(title="New Break Request")
                    requested_break.add_field(
                        name="Staff Member", value=ctx.user, inline=False
                    )
                    requested_break.add_field(
                        name="Role", value=ctx.user.top_role, inline=False
                    )

                    if duration_type == "Until further notice":
                        duration = "Until further notice"

                    elif duration_type == "Timed (1h, 1h30m, etc)":
                        parse_timespan(duration)
                        duration = duration
                    requested_break.add_field(
                        name="Duration", value=duration, inline=False
                    )
                    requested_break.add_field(name="Reason", value=reason, inline=False)
                    requested_break.set_footer(
                        text="To approve or deny this request, use `/break approve MEMBER` or `/break deny MEMBER`"
                    )
                    Break(ctx.user).add_break_request(
                        ctx.guild.id,
                        duration,
                        reason,
                        0,
                        0,
                        0,
                    )

                    await channel.send(embed=requested_break)
                    await ctx.followup.send("Break successfully requested")

    @Serverutil.command(description="Approve the break")
    @Serverutil.checks.has_any_role(core_team, om)
    async def approve(self, ctx: Interaction, member: Member):
        await ctx.response.defer(thinking=True)
        data = Break(member).check(ctx.guild.id)

        if data == None:
            await ctx.followup.send("This member never applied for break")

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't approve your own break request...")

        else:
            break_channel = await self.bot.fetch_channel(841676953613631499)
            break_log = await self.bot.fetch_channel(1001053890277556235)

            member = ctx.guild.get_member(data[0])

            accepted_break = Embed(title="Break Approved")
            accepted_break.add_field(name="Staff Member", value=member, inline=False)
            accepted_break.add_field(name="Role", value=member.top_role, inline=False)

            try:
                time = parse_timespan(data[3])
                duration = round((datetime.now() + timedelta(seconds=time)).timestamp())
                timing = "<t:{}:D>".format(duration)
                Break(member).approve(
                    ctx.guild.id, round(datetime.now().timestamp()), duration
                )
            except:
                timing = "Until further notice"
                Break(member).approve(
                    ctx.guild.id, round(datetime.now().timestamp()), 9999999999
                )

            accepted_break.add_field(name="Duration", value=timing, inline=False)
            accepted_break.add_field(name="Reason", value=data[4], inline=False)
            accepted_break.add_field(
                name="User who approved it", value=ctx.user, inline=False
            )

            break_role = ctx.guild.get_role(841682795277713498)
            await member.add_roles(break_role, reason="Staff is on break")
            await break_log.send(embed=accepted_break)

            if ctx.channel.id == 841676953613631499:
                await ctx.channel.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user
                    )
                )

            else:
                await break_channel.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user
                    )
                )
                await ctx.followup.send(f"Accepted break of {member}")

    @Serverutil.command(name="deny", description="Deny the break")
    @Serverutil.checks.has_any_role(core_team, om)
    async def _deny(self, ctx: Interaction, member: Member):
        await ctx.response.defer(thinking=True)
        if ctx.guild.id == 841671029066956831:
            data = Break(member).check(ctx.guild.id)

            if data == None:
                await ctx.followup.send("This member never applied for break")

            else:
                break_channel = await self.bot.fetch_channel(841676953613631499)

                member = ctx.guild.get_member(data[0])

                if ctx.channel.id == 841676953613631499:
                    await ctx.channel.send(
                        "{}, your break has been denied by {}".format(
                            member.mention, ctx.user
                        )
                    )

                else:
                    await ctx.followup.send(f"Denied break of {member}")
                    await break_channel.send(
                        f"{member.mention}, your break has been denied by {ctx.user}"
                    )

                Break(member).deny(ctx.guild.id)

    @Serverutil.command(name="end", description="End your break early")
    async def end(self, ctx: Interaction):
        await ctx.response.defer()
        if ctx.guild.id == 841671029066956831:
            break_role = ctx.guild.get_role(841682795277713498)

            if break_role in ctx.user.roles:
                await ctx.user.remove_roles(
                    break_role, reason="Staff returned from break"
                )
                await ctx.followup.send("Your break has ended.\nWelcome back! :tada:")
                Break(ctx.user).end(ctx.guild.id)

            else:
                await ctx.followup.send(
                    "You are not on break. Please request for a break first."
                )


class strikecog(GroupCog, name="strike"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def addstrike(
        self, ctx: Interaction, member: Member, department: str, reason: str
    ):
        channel = self.bot.get_channel(841672405444591657)
        strike = Strike(department, member)
        strike.give()

        strikes = strike.counts()

        embed = Embed(title="You have been striked", color=Color.red())
        embed.add_field(name="Department", value=department, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Strike count", value=strikes, inline=True)
        embed.set_footer(
            text="To appeal for your strike, please do `/strike appeal apply DEPARTMENT`"
        )
        await channel.send(member.mention, embed=embed)
        await ctx.followup.send("Strike given to {}".format(member))

    @Serverutil.command(
        description="Give a strike to a staff member for bad performance/unprofessionalism"
    )
    @Serverutil.checks.has_any_role(
        841671779394781225,
        841671956999045141,
        955722820464283658,
        949147158572056636,
        841682891599773767,
        962628294627438682,
        1095048263985549382,
    )
    async def give(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
        reason: str,
    ):
        await ctx.response.defer(ephemeral=True)

        CT = ctx.guild.get_role(841671779394781225)

        if CT in member.roles:
            await ctx.followup.send(
                "You can't strike someone from the {} since they have been granted strike immunity".format(
                    CT.name
                ),
                ephemeral=True,
            )

        else:
            await self.addstrike(ctx, member, department, reason)

    @Serverutil.command(
        description="Give a strike to a moderator for bad performance/unprofessionalism"
    )
    @Serverutil.describe(
        member="Which moderator?", reason="What is the reason for the strike?"
    )
    @Serverutil.checks.has_any_role(1074770189582872606)
    async def mod(self, ctx: Interaction, member: Member, reason: str):
        await ctx.response.defer(ephemeral=True)

        # mod
        MODT = ctx.guild.get_role(1075400097615052900)
        if ctx.guild.get_role(949147509660483614) in member.roles:
            await ctx.followup.send("You can't strike someone who is a CSO...")
        else:
            if MODT in member.roles:
                if ctx.user.top_role.position > MODT.position:
                    await self.addstrike(ctx, member, "Moderation", reason)

    @Serverutil.command(
        description="Remove a strike if a staff member has shown improvement"
    )
    @Serverutil.checks.has_any_role(
        core_team, chr, coo, team_leader, staff_supervisor, om
    )
    async def remove(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
        reason: str,
    ):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)

        strike = Strike(department, member)
        check = strike.check()
        if check == None:
            await ctx.followup.send("This member was never striked")
        elif check[0] != department:
            await ctx.followup.send("This member was never striked in this department")
        else:
            member = check[1]
            strike.revoke()
            strikes = strike.counts()
            m = await self.bot.fetch_user(member)

            embed = (
                Embed(title="Your strike has been removed", color=Color.green())
                .add_field(name="Strike count", value=strikes, inline=True)
                .add_field(name="Reason", value=reason, inline=True)
            )
            await channel.send(m.mention, embed=embed)

            await ctx.followup.send("Strike removed from {}".format(m))

    group2 = Serverutil.Group(name="appeal", description="...")

    @group2.command(description="Appeal your strike")
    @Serverutil.describe(
        department="Which department you were striked in?",
    )
    async def apply(
        self,
        ctx: Interaction,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
    ):
        await ctx.channel.typing()
        check = Strike(department, ctx.user).check()
        if check == None:
            await ctx.response.send_message("You were never striked")
        elif check[0] != department:
            await ctx.response.send_message("You were never striked in this department")
        else:
            await ctx.response.send_modal(Strike_Appeal(self.bot, department))

    @group2.command(description="Approve a strike appeal")
    @Serverutil.checks.has_any_role(
        core_team, om, chr, coo, team_leader, staff_supervisor
    )
    async def approve(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
    ):
        await ctx.response.defer()
        channel = self.bot.get_channel(841672405444591657)
        strike = Strike(department, member)
        user = strike.check()

        if user == None:
            await ctx.followup.send("This user has never been striked")

        elif user[0] != department:
            await ctx.followup.send("Invalid department entered")

        else:
            strike.revoke()
            staff_member = ctx.guild.get_member(user[1])
            strikes = strike.counts()

            msg = "{}, your strike appeal has been approved. You now have {} strikes".format(
                staff_member.mention, strikes
            )

            if ctx.channel.id == 841672405444591657:
                await ctx.channel.send(msg)

            else:
                await channel.send(msg)
                await ctx.followup.send("Appeal approved")

    @group2.command(description="Deny a strike appeal")
    @Serverutil.checks.has_any_role(
        core_team, om, chr, coo, team_leader, staff_supervisor
    )
    async def deny(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
    ):
        await ctx.response.defer()
        channel = self.bot.get_channel(841672405444591657)
        strike = Strike(department, member)
        user = strike.check()

        if user == None:
            await ctx.followup.send("This user was never striked")

        elif user[0] != department:
            await ctx.followup.send("Invalid department entered")

        else:
            staff_member = ctx.guild.get_member(user[1])
            msg = "{}, your strike appeal has been denied.".format(staff_member.mention)

            if ctx.channel.id == 841672405444591657:
                await ctx.channel.send(msg)

            else:
                await channel.send(msg)
                await ctx.followup.send("Appeal denied")


class resigncog(GroupCog, name="resign"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(name="apply", description="Apply for resignation")
    async def apply(self, ctx: Interaction, department: str, reason: str):
        await ctx.response.defer(ephemeral=True)
        Resign(ctx.user).resign_apply()

        channel = await self.bot.fetch_channel(1002513633760260166)

        request = Embed(
            title="Resignation request of {} | {}".format(ctx.user, ctx.user.id),
            color=ctx.user.color,
        )
        request.add_field(name="Department", value=department, inline=False)
        request.add_field(name="Reason of Resigning", value=reason, inline=False)
        request.set_footer(
            text="To accept or deny the resignation, use `/resign approve USER_ID` or `/resign approve USER_ID`"
        )

        await ctx.followup.send("Your resignation has been requested")
        await channel.send(embed=request)

    @Serverutil.command(description="Approve a resignation")
    @Serverutil.checks.has_any_role(core_team, chr, coo)
    async def approve(self, ctx: Interaction, member: Member, department: str):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672222136991757)
        resign = Resign(ctx.user)
        data = resign.check_resign()

        if data == None:
            await ctx.followup.send("Invalid User ID")

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't approve your own resignation")

        elif member.top_role >= ctx.user.top_role:
            await ctx.followup.send(
                "You cannot approve a resignation from someone who has a higher role than you"
            )

        else:
            resign.approve_resign()

        await ctx.followup.send("Accepted resignation of {}".format(member))
        await channel.send(f"{member}has resigned from {department}")

    @Serverutil.command(name="deny", description="Denies a resignation")
    @Serverutil.checks.has_any_role(core_team, chr, coo)
    async def deny(self, ctx: Interaction, member: Member):
        await ctx.response.defer(ephemeral=True)
        resign = Resign(member)
        data = resign.check_resign()

        if data == None:
            await ctx.followup.send("Invalid User ID")

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't deny your own resignation")

        elif member.top_role.position >= ctx.user.top_role.position:
            await ctx.followup.send(
                "You cannot deny a resignation from someone who has a higher role than you"
            )

        else:
            resign.deny_resign()
            try:
                await member.send("Your resignation has been denied.")
            except:
                pass
            await ctx.followup.send("Denied resignation of {}".format(member))


async def setup(bot: Bot):
    await bot.add_cog(breakcog(bot), guild=Object(id=lss))
    await bot.add_cog(strikecog(bot), guild=Object(id=lss))
    await bot.add_cog(resigncog(bot), guild=Object(id=lss))
