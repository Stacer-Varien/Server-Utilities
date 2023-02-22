from datetime import datetime, timedelta
from random import randint
from assets.menus import ProductSelect
from humanfriendly import parse_timespan
from discord import Embed, Color, Interaction, Member, CategoryChannel, Object, TextChannel
from discord import app_commands as Serverutil
from discord.ext.commands import Bot, GroupCog
from assets.functions import Break, Resign, Strike
from assets.strike_modal import Start_Appeal
from typing import Literal, Optional
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


class breakcog(GroupCog, name='break'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Apply for break")
    @Serverutil.describe(
        duration_type="Is it timed or until further notice?",
        reason="Why do you want to go on break?",
        duration=
        "If you have selected the timed option, how long are you planning to take break?"
    )
    async def apply(self,
                    ctx: Interaction,
                    duration_type: Literal["Timed (1h, 1h30m, etc)",
                                           "Until further notice"],
                    reason: str,
                    duration: Optional[str] = None) -> None:
        await ctx.response.defer()
        break_id = randint(1, 99999)
        break_role = ctx.guild.get_role(841682795277713498)
        channel = await self.bot.fetch_channel(841676953613631499)

        if break_role in ctx.user.roles:
            await ctx.followup.send("You are already on break")
        else:
            if ctx.user.id == 533792698331824138:
                break_log = await self.bot.fetch_channel(1001053890277556235)

                if duration_type == "Until further notice":
                    duration = "Until further notice"
                    Break(ctx.user).add_break_request(
                        ctx.guild.id, break_id, duration, reason, 1,
                        round(datetime.now().timestamp()), 99999999999)

                elif duration_type == "Timed (1h, 1h30m, etc)":
                    time = round((datetime.now() + timedelta(
                        seconds=parse_timespan(duration))).timestamp())
                    duration = "<t:{}:D>".format(time)
                    Break(ctx.user).add_break_request(
                        ctx.guild.id, break_id, duration, reason, 1,
                        round(datetime.now().timestamp()), time)

                own_break = Embed(description="You are now on break",
                                  color=Color.blue())
                own_break.add_field(name="Duration",
                                    value=duration,
                                    inline=False)

                await ctx.user.add_roles(break_role, reason="Owner on break")
                await channel.send(ctx.user.mention, embed=own_break)

                auto_break = Embed(title="Break Automatically Given")
                auto_break.add_field(name="Staff Member",
                                     value=ctx.user,
                                     inline=False)
                auto_break.add_field(name="Role",
                                     value=ctx.user.top_role,
                                     inline=False)
                auto_break.add_field(name="Duration",
                                     value=duration,
                                     inline=False)
                auto_break.add_field(name="Reason", value=reason, inline=False)

                await break_log.send(embed=auto_break)

            else:
                requested_break = Embed(title="New Break Request")
                requested_break.add_field(name="Staff Member",
                                          value=ctx.user,
                                          inline=False)
                requested_break.add_field(name="Role",
                                          value=ctx.user.top_role,
                                          inline=False)

                if duration_type == "Until further notice":
                    duration = "Until further notice"

                elif duration_type == "Timed (1h, 1h30m, etc)":
                    parse_timespan(duration)
                    duration = duration
                requested_break.add_field(name="Duration",
                                          value=duration,
                                          inline=False)
                requested_break.add_field(name="Reason",
                                          value=reason,
                                          inline=False)
                requested_break.add_field(name="Break ID",
                                          value=break_id,
                                          inline=False)
                requested_break.set_footer(
                    text=
                    "To approve or deny this request, use `/staff_break approve BREAK_ID` or `/staff_break deny BREAK_ID`"
                )
                Break(ctx.user).add_break_request(
                    ctx.guild.id,
                    break_id,
                    duration,
                    reason,
                    0,
                    0,
                    0,
                )

                await channel.send(embed=requested_break)
                await ctx.followup.send("Break successfully requested",
                                        delete_after=10.0)

    @Serverutil.command(description="Approve the break")
    @Serverutil.checks.has_any_role(core_team, om)
    async def approve(self, ctx: Interaction, break_id: int):
        await ctx.response.defer()
        data = Break().fetch_break_id(break_id, ctx.guild.id)

        if data == None:
            await ctx.followup.send("Invalid break ID passed",
                                    delete_after=10.0)

        elif data[0] == ctx.user.id:
            await ctx.followup.send(
                "You can't approve your own break request....",
                delete_after=10.0)

        else:
            break_channel = await self.bot.fetch_channel(841676953613631499)
            break_log = await self.bot.fetch_channel(1001053890277556235)

            member = ctx.guild.get_member(data[0])

            accepted_break = Embed(title="Break Approved")
            accepted_break.add_field(name="Staff Member",
                                     value=member,
                                     inline=False)
            accepted_break.add_field(name="Role",
                                     value=member.top_role,
                                     inline=False)

            try:
                time = parse_timespan(data[3])
                duration = round(
                    (datetime.now() + timedelta(seconds=time)).timestamp())
                timing = "<t:{}:D>".format(duration)
                Break(member).approve_break(ctx.guild.id,
                                            round(datetime.now().timestamp()),
                                            duration)
            except:
                timing = "Until further notice"
                Break(member).approve_break(ctx.guild.id,
                                            round(datetime.now().timestamp()),
                                            9999999999)

            accepted_break.add_field(name="Duration",
                                     value=timing,
                                     inline=False)
            accepted_break.add_field(name="Reason",
                                     value=data[4],
                                     inline=False)
            accepted_break.add_field(name="User who approved it",
                                     value=ctx.user,
                                     inline=False)

            break_role = ctx.guild.get_role(841682795277713498)
            await member.add_roles(break_role, reason="Staff is on break")
            await break_log.send(embed=accepted_break)

            if ctx.channel.id == 841676953613631499:
                await ctx.followup.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user))

            else:

                await break_channel.send(
                    "{}, your break has been approved by {}".format(
                        member.mention, ctx.user))
                await ctx.followup.send(f"Accepted break of {member}",
                                        delete_after=10.0)

    @Serverutil.command(name="deny", description="Deny the break")
    @Serverutil.checks.has_any_role(core_team, om)
    async def _deny(self, ctx: Interaction, break_id: int):
        await ctx.response.defer()
        if ctx.guild.id == 841671029066956831:
            data = Break().fetch_break_id(break_id, ctx.guild.id)

            if data == None:
                await ctx.followup.send("Invalid break ID passed",
                                        delete_after=10.0)

            else:
                break_channel = await self.bot.fetch_channel(841676953613631499
                                                             )

                member = ctx.guild.get_member(data[0])

                if ctx.channel.id == 841676953613631499:
                    await ctx.followup.send(
                        "{}, your break has been denied by {}".format(
                            member.mention, ctx.user))

                else:
                    await ctx.followup.send(f"Denied break of {member}",
                                            delete_after=10.0)
                    await break_channel.send(
                        f"{member.mention}, your break has been denied by {ctx.user}"
                    )

                Break().deny_break(break_id, ctx.guild.id)

    @Serverutil.command(name='end', description="End your break early")
    async def end(self, ctx: Interaction):
        await ctx.response.defer()
        if ctx.guild.id == 841671029066956831:
            break_role = ctx.guild.get_role(841682795277713498)

            if break_role in ctx.user.roles:
                await ctx.user.remove_roles(break_role,
                                            reason="Staff returned from break")
                await ctx.followup.send(
                    "Your break has ended.\nWelcome back! :tada:",
                    delete_after=10.0)
                Break(ctx.user).end_break(ctx.guild.id)

            else:
                await ctx.followup.send(
                    "You are not on break. Please request for a break first.",
                    delete_after=10.0)


class strikecog(GroupCog, name='strike'):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def addstrike(self, ctx: Interaction, member: Member,
                        department: str, reason: str, strike: Strike):
        channel = self.bot.get_channel(841672405444591657)
        strike_id = randint(0, 99999)
        appeal_id = randint(0, 99999)
        strike.give(strike_id, appeal_id)
        if strike.get_strikes() == None:
            strikes = 0
        else:
            strikes = strike.get_strikes()

        embed = Embed(title="You have been striked", color=Color.red())
        embed.add_field(name="Strike count", value=strikes, inline=True)
        embed.add_field(name="Department", value=department, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Strike ID", value=strike_id)
        embed.set_footer(
            text=
            "To appeal for your strike, please do `/strike appeal STRIKE ID`")
        await channel.send(member.mention, embed=embed)
        await ctx.followup.send("Strike given to {}".format(member))

    @Serverutil.command(
        description=
        "Give a strike to a staff member for bad performance/unprofessionalism"
    )
    async def give(self, ctx: Interaction, member: Member,
                   department: Literal["Management", "Human Resources",
                                       "Moderation", "Marketing"],
                   reason: str):
        await ctx.response.defer(ephemeral=True)

        #all
        CT = ctx.guild.get_role(841671779394781225)
        OM = ctx.guild.get_role(841671956999045141)
        COO = ctx.guild.get_role(955722820464283658)
        CHR = ctx.guild.get_role(949147158572056636)
        TL = ctx.guild.get_role(841682891599773767)
        SS = ctx.guild.get_role(962628294627438682)

        #mod
        CSO = ctx.guild.fetch_roles(949147509660483614)
        CAO = ctx.guild.get_role(1076650317392916591)
        CSOA = ctx.guild.get_role(1074770323293085716)
        CSOT = ctx.guild.get_role(1074770253294342144)
        MODS = ctx.guild.get_role(1074770253294342144)
        MODT = ctx.guild.get_role(1074770253294342144)

        ALL = [CT, OM, COO, CHR, TL, SS]

        if CT in member.roles:
            await ctx.followup.send(
                "You can't strike someone from the {} since they have been granted strike immunity"
                .format(CT.name),
                ephemeral=True)

        else:
            if department == 'Moderation':
                if MODT in ctx.user.roles and MODT in member.roles:
                    MODERS = [CSO, CAO, CSOA, CSOT, MODS]
                    if any(role.id for role in MODERS
                           for role in ctx.user.roles):
                        if ctx.user.get_role(CSO).position >= member.get_role(
                                CAO
                        ) or ctx.user.get_role(CAO).position >= member.get_role(
                                CSOA).position or ctx.user.get_role(
                                    CSOA).position >= member.get_role(
                                        CSOT).position or ctx.user.get_role(
                                            CSOT).position >= member.get_role(
                                                MODS
                                            ).position or ctx.user.get_role(
                                                MODS
                                            ).position > member.get_role(
                                                1074770103415083099).position:
                            strike = Strike(department, member)
                    await self.addstrike(ctx, member, department, reason,
                                         strike)
            elif department == "Marketing":
                if ctx.user.get_role(
                        950013921895538688).position > member.get_role(
                            881084354422538281).position:
                    strike = Strike(department, member)
                    await self.addstrike(ctx, member, department, reason,
                                         strike)

            elif any(role.id for role in ALL for role in ctx.user.roles):
                strike = Strike(department, member)
                await self.addstrike(ctx, member, department, reason, strike)

            else:
                await ctx.followup.send(
                    "You do not have the required roles to do a strike")

    @Serverutil.command(
        description="Remove a strike if a staff member has shown improvement")
    @Serverutil.checks.has_any_role(core_team, chr, coo, team_leader,
                                    staff_supervisor, om)
    async def remove(self, ctx: Interaction, strike_id: int,
                     department: Literal["Management", "Human Resources",
                                         "Moderation", "Marketing"],
                     reason: str):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)

        strike = Strike(department)
        check = strike.check_id(strike_id)
        if check == None:
            await ctx.followup.send("Strike ID does not exist")
        else:
            member = check[1]
            strike.revoke(strike_id)
            strikes = Strike(department, member).get_strikes()
            m = await self.bot.fetch_user(member)

            embed = Embed(title="Your strike has been removed",
                          color=Color.green()).add_field(
                              name="Strike count", value=strikes,
                              inline=True).add_field(name="Reason",
                                                     value=reason,
                                                     inline=True)
            await channel.send(m.mention, embed=embed)

            await ctx.followup.send("Strike removed from {}".format(m))

    @Serverutil.command(description="Appeal your strike")
    @Serverutil.describe(
        strike_id="Enter the strike ID you wish to appeal here",
        department="Which department you were striked in?")
    async def appeal(self, ctx: Interaction, strike_id: int,
                     department: Literal["Management", "Human Resources",
                                         "Moderation", "Marketing"]):
        view = Start_Appeal(self.bot, strike_id, department)
        msg = """
Before you start appealing your strike, please make sure:
    1. Your reason is valid and accurate
    2. You have proof in media links if necessary
        
If you feel it meets those conditions, click the button below.
Also just to let you know, your user ID is logged when doing this appeal so if you troll, we will take actions.
"""

        await ctx.response.send_message(msg, view=view, ephemeral=True)

    @Serverutil.command(description="Approve or deny a strike")
    @Serverutil.checks.has_any_role(core_team, chr, coo, team_leader,
                                    staff_supervisor)
    async def appealverdict(self, ctx: Interaction, strike_appeal_id: int,
                            department: Literal["Management",
                                                "Human Resources",
                                                "Moderation", "Marketing"],
                            verdict: Literal["accept", "deny"]):
        await ctx.response.defer()
        channel = self.bot.get_channel(841672405444591657)
        strike = Strike(department)
        user = strike.fetch_striked_staff(strike_appeal_id)

        if user == None:
            await ctx.followup.send("Invalid Strike Appeal ID passed",
                                    delete_after=5)

        elif user[0] != department:
            await ctx.followup.send("Invalid department entered",
                                    delete_after=5)

        else:
            if verdict == "accept":
                strike.revoke(user[2])

                strikes = strike.get_strikes(user[1])

                staff_member = ctx.guild.get_member(user[1])
                msg = "{}, your appeal for your strike has been appealled. You now have {} strikes".format(
                    staff_member.mention, strikes)

            elif verdict == "deny":
                staff_member = ctx.guild.get_member(user[1])
                msg = "{}, your appeal for your strike has been denied.".format(
                    staff_member.mention)

            if ctx.channel.id == 841672405444591657:
                await ctx.followup.send(msg)

            else:
                await channel.send(msg)
                await ctx.followup.send("Verdict given to appeal")


class resigncog(GroupCog, name='resign'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(name="apply", description="Apply for resignation")
    async def apply(self, ctx: Interaction, department: str, reason: str):
        await ctx.response.defer(ephemeral=True)
        Resign(ctx.user).resign_apply(ctx.user)

        channel = self.bot.get_channel(1002513633760260166)

        request = Embed(title="Resignation request of {} | {}".format(
            ctx.user, ctx.user.id),
                        color=ctx.user.color)
        request.add_field(name="Department", value=department, inline=False)
        request.add_field(name="Reason of Resigning",
                          value=reason,
                          inline=False)
        request.set_footer(
            text=
            "To accept or deny the resignation, use `/resign approve USER_ID` or `/resign approve USER_ID`"
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

        elif member.top_role >= ctx.user.top_role:
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


class pricelistcog():

    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Get a list of LOA coin pricelist")
    async def loacoins(self, ctx: Interaction):
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)

        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                view = ProductSelect()
                embed = Embed()
                embed.color = Color.blue()
                embed.description = "Use the dropmenu below to view a package"
                await ctx.response.send_message(embed=embed, view=view)

    @Serverutil.command(description="Get a list of LOA coin pricelist")
    async def paidplans(self, ctx: Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                embed = Embed(color=Color.blue())
                embed.title = "Paid plans"
                embed.description = """
$3 Nitro:
- Giveaway with prize provided by us (or by your side if you are willing to), 7 days
- Custom Channel with Shoutout Ping + Partner Ping
- 10000 LOA Coins
- Premium Role for a month

$10 Nitro:
- Fully customisable package base on your server type and size 
What you can get for getting any of our plans:
- ⭐ Shiny high up Buyers role
- 🌟 Giveaway bonus entries
"""

    @Serverutil.command(description="Get a list of LOA booster plans")
    async def boosts(self, ctx: Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                embed = Embed(color=Color.blue())
                embed.title = "Booster plans"
                embed.description = """
♦️1 Boost
- Premium Membership until your boosts end
- Shoutout with Shoutout Ping + Partner Ping
- 5000 LOA Coins
- LOA Booster role
- Massive thank you
- Giveaway bonus entries

♦️♦️ 2 Boosts

- All above perks
- 8000 LOA Coins
- Auto advertisement in Open Network every 4 hours
- Legendary Booster Role

♦️ ♦️ ♦️ 3 boosts
-All above perks
-Auto Advertisement in Open Network upgrade to every 1 hour (worth 40k LOA Coins)
-12000 LOA Coins 
"""
                await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(breakcog(bot), guild=Object(id=lss))
    await bot.add_cog(strikecog(bot), guild=Object(id=lss))
    await bot.add_cog(resigncog(bot), guild=Object(id=lss))
    await bot.add_cog(pricelistcog(bot), guild=Object(id=lss))
