from datetime import datetime, timedelta
from typing import Literal, Optional

from discord import app_commands as Serverutil
from discord import Embed, Color, Interaction, Member, Object
from discord.ext.commands import Bot, GroupCog
from humanfriendly import parse_timespan

from assets.functions import Break, Resign, Strike
from assets.strike_modal import StrikeAppeal
from config import lss

ha_admin = 925790259319558157
ha_hr = 925790259319558156
ha_mod = 925790259319558154
core_team = 841671779394781225  # both
coo = 955722820464283658  # strike + resign
chr = 949147158572056636  # strike + resign
team_leader = 841682891599773767  # strike
staff_supervisor = 962628294627438682  # strike
om = 841671956999045141  # break


class BreakCog(GroupCog, name="break"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Apply to go on break until you come back")
    @Serverutil.describe(
        reason="Why do you want to go on break?",
        duration="How long are you planning to take break? (1d, 3 days, etc)",
    )
    async def apply(self, ctx: Interaction, reason: str, duration: str) -> None:
        await ctx.response.defer()
        break_role = ctx.guild.get_role(841682795277713498)
        channel = await self.bot.fetch_channel(841676953613631499)

        if break_role in ctx.user.roles:
            await ctx.followup.send("You are already on break")
        else:
            if ctx.user.id == 1033533294840664074:
                break_log = await self.bot.fetch_channel(1001053890277556235)
                time = round(
                    (
                        datetime.now() + timedelta(seconds=parse_timespan(duration))
                    ).timestamp()
                )
                duration = "<t:{}:D>".format(time)
                await Break(ctx.user).add_request(
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
                auto_break.add_field(name="Staff Member", value=ctx.user, inline=False)
                auto_break.add_field(name="Duration", value=duration, inline=False)
                auto_break.add_field(name="Reason", value=reason, inline=False)

                await break_log.send(embed=auto_break)
            else:
                parse_timespan(duration)
                requested_break = Embed(title="New Break Request")
                requested_break.add_field(
                    name="Staff Member", value=ctx.user, inline=False
                )

                requested_break.add_field(name="Duration", value=duration, inline=False)
                requested_break.add_field(name="Reason", value=reason, inline=False)
                requested_break.set_footer(
                    text="To approve or deny this request, use `/break approve MEMBER` or `/break deny MEMBER`"
                )
                await Break(ctx.user).add_request(
                    ctx.guild.id,
                    duration,
                    reason,
                    0,
                    0,
                    0,
                )
                await ctx.followup.send("Break successfully requested")
                await channel.send(embed=requested_break)

    @apply.error
    async def apply_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.CommandInvokeError):
            await ctx.followup.send(
                embed=Embed(description=str(error), color=Color.red())
            )

    @Serverutil.command(description="Approve the break")
    @Serverutil.checks.has_any_role(core_team, om, 995151171004137492)
    async def approve(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        data = Break(member).check(ctx.guild.id)

        if data is None:
            await ctx.followup.send("This member never applied for break")

        elif int(data[0]) == ctx.user.id:
            await ctx.followup.send("You can't approve your own break request...")

        else:
            break_channel = await self.bot.fetch_channel(841676953613631499)
            break_log = await self.bot.fetch_channel(1001053890277556235)

            member = ctx.guild.get_member(int(data[0]))

            accepted_break = Embed(title="Break Approved")
            accepted_break.add_field(name="Staff Member", value=member, inline=False)

            time = parse_timespan(str(data[2]))
            duration = round((datetime.now() + timedelta(seconds=time)).timestamp())
            timing = "<t:{}:D>".format(duration)
            await Break(member).approve(
                ctx.guild.id, round(datetime.now().timestamp()), duration
            )

            accepted_break.add_field(name="Duration", value=timing, inline=False)
            accepted_break.add_field(name="Reason", value=str(data[3]), inline=False)
            accepted_break.add_field(
                name="User who approved it", value=ctx.user, inline=False
            )

            break_role = ctx.guild.get_role(841682795277713498)
            await member.add_roles(break_role, reason="Staff is on break")
            await break_log.send(embed=accepted_break)

            if ctx.channel.id == 841676953613631499:
                await ctx.followup.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user
                    )
                )

            else:
                await ctx.followup.send(f"Accepted break of {member}")
                await break_channel.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user
                    )
                )

    @Serverutil.command(name="deny", description="Deny the break")
    @Serverutil.checks.has_any_role(core_team, om, 995151171004137492)
    async def _deny(self, ctx: Interaction, member: Member):
        await ctx.response.defer(thinking=True)
        if ctx.guild.id == 841671029066956831:
            data = Break(member).check(ctx.guild.id)

            if data is None:
                await ctx.followup.send("This member never applied for break")

            else:
                break_channel = await self.bot.fetch_channel(841676953613631499)

                member = ctx.guild.get_member(int(data[0]))

                if ctx.channel.id == 841676953613631499:
                    await ctx.followup.send(
                        "{}, your break has been denied by {}".format(
                            member.mention, ctx.user
                        )
                    )

                else:
                    await ctx.followup.send(f"Denied break of {member}")
                    await break_channel.send(
                        f"{member.mention}, your break has been denied by {ctx.user}"
                    )

                await Break(member).deny(ctx.guild.id)

    @Serverutil.command(name="cancel", description="Cancel your break request")
    async def cancel(self, ctx: Interaction):
        await ctx.response.defer(thinking=True)
        if ctx.guild.id == 841671029066956831:
            data = Break(ctx.user).check(ctx.guild.id)

            if data is None:
                await ctx.followup.send("You haven't applied for a break")
                return
            embed = Embed(
                description="Break canceled and removed", color=Color.random()
            )
            await Break(ctx.user).cancel(ctx.guild.id)
            await ctx.followup.send(embed=embed)

    @approve.error
    async def approve_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.MissingAnyRole):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.followup.send(embed=embed)

    @_deny.error
    async def _deny_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.MissingAnyRole):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.followup.send(embed=embed)

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
                await Break(ctx.user).end(ctx.guild.id)
                return

            await ctx.followup.send(
                "You are not on break. Please request for a break first."
            )


class StrikeCog(GroupCog, name="strike"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def addstrike(
        self, ctx: Interaction, member: Member, department: str, reason: str
    ):
        channel = self.bot.get_channel(841672405444591657)
        strike = Strike(department, member)
        await strike.give()

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
        841671779394781225, 1095048263985549382, 1072103843569094796, 841671956999045141
    )
    async def give(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal["Management", "Human Resources", "Moderation", "Marketing"],
        reason: str,
    ):
        await ctx.response.defer(ephemeral=True)

        coreteam = ctx.guild.get_role(841671779394781225)

        if coreteam in member.roles:
            await ctx.followup.send(
                "You can't strike someone from the {} since they have been granted strike immunity".format(
                    coreteam.name
                ),
                ephemeral=True,
            )
            return

        await self.addstrike(ctx, member, department, reason)

    @Serverutil.command(
        description="Give a strike to a moderator for bad performance/unprofessionalism"
    )
    @Serverutil.describe(
        member="Which moderator?", reason="What is the reason for the strike?"
    )
    @Serverutil.checks.has_any_role(
        1074770189582872606,
        1074770253294342144,
        1074770323293085716,
        841671956999045141,
        1095048263985549382,
        841671779394781225,
        949147509660483614,
    )
    async def mod(self, ctx: Interaction, member: Member, reason: str):
        await ctx.response.defer(ephemeral=True)

        # mod
        moddept = ctx.guild.get_role(1075400097615052900)
        cso = ctx.guild.get_role(949147509660483614)
        if cso in member.roles:
            await ctx.followup.send(f"You can't strike someone who is a {cso.name}...")
        else:
            if moddept in member.roles:
                if ctx.user.top_role.position > moddept.position:
                    await self.addstrike(ctx, member, "Moderation", reason)

    @Serverutil.command(
        description="Remove a strike if a staff member has shown improvement"
    )
    @Serverutil.checks.has_any_role(
        core_team, chr, coo, team_leader, staff_supervisor, om, 1095048263985549382
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
        if check is None:
            await ctx.followup.send("This member was never striked")
            return
        if check[0] != department:
            await ctx.followup.send("This member was never striked in this department")
            return

        await strike.revoke()
        strikes = strike.counts()

        embed = (
            Embed(title="Your strike has been removed", color=Color.green())
            .add_field(name="Strike count", value=strikes, inline=True)
            .add_field(name="Reason", value=reason, inline=True)
        )
        await channel.send(member.mention, embed=embed)

        await ctx.followup.send("Strike removed from {}".format(member))

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
        if check is None:
            await ctx.response.send_message("You were never striked")
            return
        if check[0] != department:
            await ctx.response.send_message("You were never striked in this department")
            return
        await ctx.response.send_modal(StrikeAppeal(self.bot, department))

    @group2.command(description="Approve a strike appeal")
    @Serverutil.checks.has_any_role(
        841671779394781225, 1095048263985549382, 1072103843569094796, 841671956999045141
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

        if user is None:
            await ctx.followup.send("This user has never been striked")
            return

        elif str(user[0]) != department:
            await ctx.followup.send("Invalid department entered")
            return

        await strike.revoke()
        staff_member = ctx.guild.get_member(int(user[1]))
        strikes = strike.counts()

        msg = (
            "{}, your strike appeal has been approved. You now have {} strikes".format(
                staff_member.mention, strikes
            )
        )

        if ctx.channel.id == 841672405444591657:
            await ctx.channel.send(msg)
            return

        await channel.send(msg)
        await ctx.followup.send("Appeal approved")

    @group2.command(description="Deny a strike appeal")
    @Serverutil.checks.has_any_role(
        841671779394781225, 1095048263985549382, 1072103843569094796, 841671956999045141
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

        if user is None:
            await ctx.followup.send("This user was never striked")
            return

        if str(user[0]) != department:
            await ctx.followup.send("Invalid department entered")
            return

        staff_member = ctx.guild.get_member(int(user[1]))
        msg = "{}, your strike appeal has been denied.".format(staff_member.mention)

        if ctx.channel.id == 841672405444591657:
            await ctx.channel.send(msg)
            return

        await channel.send(msg)
        await ctx.followup.send("Appeal denied")


class ResignCog(GroupCog, name="resign"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(name="apply", description="Apply for resignation")
    async def apply(
        self,
        ctx: Interaction,
        department: Literal[
            "Core Team", "Management", "Marketing", "Human Resource", "Moderator"
        ],
        reason: str,
        planning_to_leave: Optional[bool] = None,
    ):
        await ctx.response.defer(ephemeral=True)
        Resign(ctx.user).apply(planning_to_leave)

        channel = await ctx.guild.fetch_channel(1002513633760260166)

        request = Embed(
            title="Resignation request of {} | {}".format(ctx.user, ctx.user.id),
            color=Color.random(),
        )
        request.add_field(name="Department", value=department, inline=False)
        request.add_field(name="Reason of Resigning", value=reason, inline=False)
        if planning_to_leave == False or planning_to_leave == None:
            request.add_field(name="Plans to leave LSS", value="No", inline=False)
        else:
            request.add_field(name="Plans to leave LSS", value="Yes", inline=False)
        request.set_footer(
            text="To accept or deny the resignation, use `/resign approve MEMBER` or `/resign deny MEMBER`"
        )
        await channel.send(embed=request)
        await ctx.followup.send("Your resignation has been requested")

    @Serverutil.command(description="Approve a resignation")
    @Serverutil.checks.has_any_role(core_team, chr, coo)
    async def approve(
        self,
        ctx: Interaction,
        member: Member,
        department: Literal[
            "Core Team", "Management", "Marketing", "Human Resource", "Moderator", "All"
        ],
        leaving: Optional[bool] = None,
    ):
        await ctx.response.defer(ephemeral=True)
        channel = await ctx.guild.fetch_channel(841672222136991757)
        resign = Resign(member)
        if leaving is None or leaving is False:
            leaving = 0
        else:
            leaving = 1

        data = resign.check(leaving)

        if data is None:
            await ctx.followup.send("Invalid Member")

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't approve your own resignation")
            return

        if member.top_role >= ctx.user.top_role:
            await ctx.followup.send(
                "You cannot approve a resignation from someone who has a higher role than you"
            )
            return

        await resign.approve()
        await ctx.followup.send("Accepted resignation of {}".format(member))
        if int(data[2]) == 1:
            await channel.send(
                f"{member.mention} has made a full resignation. Thank you for working with us"
            )
            return

        if int(data[2]) == 0:
            await channel.send(f"{member.mention} has resigned from {department}")

    @Serverutil.command(name="deny", description="Denies a resignation")
    @Serverutil.checks.has_any_role(core_team, chr, coo)
    async def deny(self, ctx: Interaction, member: Member):
        await ctx.response.defer(ephemeral=True)
        resign = Resign(member)
        data = resign.check()

        if data is None:
            await ctx.followup.send("Invalid User ID")
            return

        if data[0] == ctx.user.id:
            await ctx.followup.send("You can't deny your own resignation")
            return

        if member.top_role.position >= ctx.user.top_role.position:
            await ctx.followup.send(
                "You cannot deny a resignation from someone who has a higher role than you"
            )
            return

        await resign.deny()
        try:
            await member.send("Your resignation has been denied.")
        except:
            pass
        await ctx.followup.send("Denied resignation of {}".format(member.mention))


async def setup(bot: Bot):
    await bot.add_cog(BreakCog(bot), guild=Object(id=lss))
    await bot.add_cog(StrikeCog(bot), guild=Object(id=lss))
    await bot.add_cog(ResignCog(bot), guild=Object(id=lss))
