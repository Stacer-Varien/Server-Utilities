from datetime import datetime, timedelta
from random import randint
from nextcord.utils import get

from humanfriendly import parse_timespan
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import has_any_role
from nextcord.ext.commands import Cog, Bot

from assets.functions import check_strike_id, fetch_striked_staff, get_strikes, revoke_strike, strike_staff
from assets.strike_modal import Start_Appeal
from config import db

ha_admin = 925790259319558157
ha_hr = 925790259319558156
ha_mod = 925790259319558154
core_team = 841671779394781225  # both
coo = 955722820464283658  # strike + resign
chr = 949147158572056636  # strike + resign
team_leader = 841682891599773767  # strike
staff_supervisor = 962628294627438682  # strike
om = 841671956999045141  # break


class staff_mngm(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash(description="Main staff break command", guild_ids=[841671029066956831])
    async def staff_break(self, ctx: Interaction):
        pass

    @staff_break.subcommand(description="Apply for break")
    async def apply(self, ctx: Interaction,
                    duration_type=SlashOption(description="Is it timed or until further notice?",
                                              choices=["Timed (1h, 1h30m, etc)", "Until further notice"],
                                              required=True),
                    reason=SlashOption(description="Why do you want to go on break?", required=True),
                    duration=SlashOption(
                        description="If you have selected the timed option, how long are you planning to take break?",
                        required=False)):
        await ctx.response.defer()
        break_id = randint(1, 99999)
        break_role = ctx.guild.get_role(841682795277713498)
        channel = await self.bot.fetch_channel(841676953613631499)

        if break_role in ctx.user.roles:
            await ctx.followup.send("You are already on break")

        elif ctx.user.id == 533792698331824138:
            break_log = await self.bot.fetch_channel(1001053890277556235)

            if duration_type == "Until further notice":
                duration = "Until further notice"
                db.execute(
                    "INSERT OR IGNORE INTO breakData (user_id, guild_id, break_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?,?)",
                    (533792698331824138, ctx.guild.id, break_id, duration, reason, 1,
                     (round(datetime.now().timestamp()), 999999999999999,)))
                db.commit()


            elif duration_type == "Timed (1h, 1h30m, etc)":
                time = round(
                    (datetime.now() + timedelta(seconds=parse_timespan(duration))).timestamp())
                duration = "<t:{}:D>".format(time)

                db.execute(
                    "INSERT OR IGNORE INTO breakData (user_id, guild_id, break_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?,?)",
                    (533792698331824138, ctx.guild.id, break_id, duration, reason, 1,
                     (round(datetime.now().timestamp()), time,)))
                db.commit()

            own_break = Embed(description="You are now on break", color=Color.blue())
            own_break.add_field(name="Duration", value=duration, inline=False)

            await ctx.user.add_roles(break_role, reason="Owner on break")
            await channel.send(ctx.user.mention, embed=own_break)

            auto_break = Embed(title="Break Automatically Given")
            auto_break.add_field(
                name="Staff Member", value=ctx.user, inline=False)
            auto_break.add_field(
                name="Role", value=ctx.user.top_role, inline=False)
            auto_break.add_field(
                name="Duration", value=duration, inline=False)
            auto_break.add_field(
                name="Reason", value=reason, inline=False)

            await break_log.send(embed=auto_break)

        else:
            requested_break = Embed(title="New Break Request")
            requested_break.add_field(
                name="Staff Member", value=ctx.user, inline=False)
            requested_break.add_field(
                name="Role", value=ctx.user.top_role, inline=False)

            if duration_type == "Until further notice":
                duration = "Until further notice"

            elif duration_type == "Timed (1h, 1h30m, etc)":
                parse_timespan(duration)
                duration = duration
            requested_break.add_field(
                name="Duration", value=duration, inline=False)
            requested_break.add_field(
                name="Reason", value=reason, inline=False)
            requested_break.add_field(
                name="Break ID", value=break_id, inline=False)
            requested_break.set_footer(
                text="To approve or deny this request, use `/staff_break approve BREAK_ID` or `/staff_break deny BREAK_ID`")
            db.execute(
                "INSERT OR IGNORE INTO breakData (user_id, guild_id, break_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?,?)",
                (ctx.user.id, ctx.guild.id, break_id, duration, reason, 0, 0, 0,))
            db.commit()

            await channel.send(embed=requested_break)
            await ctx.followup.send("Break successfully requested", delete_after=10.0)

    @staff_break.subcommand(name="approve", description="Approve the break")
    @has_any_role(core_team, om)
    async def _approve(self, ctx: Interaction, break_id=SlashOption(required=True)):
        await ctx.response.defer()
        data = db.execute("SELECT * FROM breakData WHERE break_id = ? AND guild_id = ?",
                          (break_id, ctx.guild.id,)).fetchone()

        if data == None:
            await ctx.followup.send("Invalid break ID passed", delete_after=10.0)

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't approve your own break request....", delete_after=10.0)

        else:
            break_channel = await self.bot.fetch_channel(841676953613631499)
            break_log = await self.bot.fetch_channel(1001053890277556235)

            member = ctx.guild.get_member(data[0])

            accepted_break = Embed(title="Break Approved")
            accepted_break.add_field(
                name="Staff Member", value=member, inline=False)
            accepted_break.add_field(
                name="Role", value=member.top_role, inline=False)

            try:
                time = parse_timespan(data[3])
                duration = round((datetime.now() + timedelta(seconds=time)).timestamp())
                timing = "<t:{}:D>".format(duration)
                db.execute("UPDATE breakData SET accepted = ? WHERE user_id = ? and guild_id = ?",
                           (1, member.id, ctx.guild.id,))
                db.execute("UPDATE breakData SET start = ? WHERE user_id = ? and guild_id = ?",
                           (round(datetime.now().timestamp()), member.id, ctx.guild.id,))
                db.execute("UPDATE breakData SET ends = ? WHERE user_id = ? and guild_id = ?",
                           (duration, member.id, ctx.guild.id,))
                db.commit()
            except:
                timing = "Until further notice"
                db.execute("UPDATE breakData SET accepted = ? WHERE user_id = ? and guild_id = ?",
                           (1, member.id, ctx.guild.id,))
                db.execute("UPDATE breakData SET start = ? WHERE user_id = ? and guild_id = ?", (round(
                    datetime.now().timestamp()), member.id, ctx.guild.id,))
                db.execute("UPDATE breakData SET ends = ? WHERE user_id = ? and guild_id = ?",
                           (9999999999, member.id, ctx.guild.id,))

            accepted_break.add_field(
                name="Duration", value=timing, inline=False)
            accepted_break.add_field(
                name="Reason", value=data[4], inline=False)
            accepted_break.add_field(
                name="User who approved it", value=ctx.user, inline=False)

            break_role = ctx.guild.get_role(841682795277713498)
            await member.add_roles(break_role, reason="Staff is on break")
            await break_log.send(embed=accepted_break)

            if ctx.channel.id == 841676953613631499:
                await ctx.followup.send("{}, your break has been approved by {}".format(member.mention, ctx.user))

            else:

                await break_channel.send("{}, your break has been approved by {}".format(member.mention, ctx.user))
                await ctx.followup.send(f"Accepted break of {member}", delete_after=10.0)

            db.commit()

    @staff_break.subcommand(name="deny", description="Deny the break")
    @has_any_role(core_team, om)
    async def _deny(self, ctx: Interaction, break_id=SlashOption(required=True)):
        await ctx.response.defer()
        if ctx.guild.id == 841671029066956831:
            data = db.execute(
                "SELECT * FROM breakData WHERE break_id = ? and guild_id = ?", (break_id, ctx.guild.id,)).fetchone()

            if data == None:
                await ctx.followup.send("Invalid break ID passed", delete_after=10.0)

            else:
                break_channel = await self.bot.fetch_channel(841676953613631499)

                member = ctx.guild.get_member(data[0])

                if ctx.channel.id == 841676953613631499:
                    await ctx.followup.send("{}, your break has been denied by {}".format(member.mention, ctx.user))

                else:
                    await ctx.followup.send(f"Denied break of {member}", delete_after=10.0)
                    await break_channel.send(f"{member.mention}, your break has been denied by {ctx.user}")

                db.execute(
                    "DELETE FROM breakData WHERE break_id = ? and guild_id = ?", (break_id, ctx.guild.id,))
                db.commit()

    @staff_break.subcommand(name='end', description="End your break")
    async def _end(self, ctx: Interaction):
        await ctx.response.defer()
        if ctx.guild.id == 841671029066956831:
            break_role = ctx.guild.get_role(841682795277713498)

            if break_role in ctx.user.roles:
                await ctx.user.remove_roles(break_role, reason="Staff returned from break")
                await ctx.followup.send("Your break has ended.\nWelcome back! :tada:", delete_after=10.0)
                db.execute(
                    "DELETE FROM breakData WHERE user_id = ? and guild_id = ?", (ctx.user.id, ctx.guild.id,))
                db.commit()

            else:
                await ctx.followup.send("You are not on break. Please request for a break first.", delete_after=10.0)

    @slash(description="Main strike command", guild_ids=[841671029066956831])
    async def strike(self, ctx: Interaction):
        pass

    @strike.subcommand(description="Give a strike to a staff member for bad performance")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def give(self, ctx: Interaction, member: Member = SlashOption(required=True), department=SlashOption(
        choices=["Management", "Human Resources", "Moderation", "Marketing"], required=True),
                   reason=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)
        CT = ctx.guild.get_role(core_team)

        if CT in member.roles:
            await ctx.followup.send(
                "You can't strike someone from the Core Team since they have been granted strike immunity",
                ephemeral=True)

        else:
            strike_id = randint(0, 99999)
            appeal_id = randint(0, 99999)
            strike_staff(department, member.id, strike_id, appeal_id)
            strikes = len(get_strikes(department, member.id))

            embed = Embed(title="You have been striked", color=Color.red())
            embed.add_field(name="Strike count", value=strikes, inline=True)
            embed.add_field(name="Department", value=department, inline=True)
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.add_field(name="Strike ID", value=strike_id)
            embed.set_footer(text="To appeal for your strike, please do `/strike appeal STRIKE ID`")
            await channel.send(member.mention, embed=embed)
            await ctx.followup.send("Strike given to {}".format(member))

    @strike.subcommand(description="Remove a strike if a staff member has shown improvement")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def remove(self, ctx: Interaction, strike_id=SlashOption(required=True), department=SlashOption(
        choices=["Management", "Human Resources", "Moderation", "Marketing"], required=True),
                     reason=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)

        check = check_strike_id(strike_id, department)

        if check == None:
            await ctx.followup.send("Strike ID does not exist")
        else:
            member = check[1]
            revoke_strike(department, strike_id)
            strikes = len(get_strikes(department, member, ))
            m = await self.bot.fetch_user(member)

            embed = Embed(title="Your strike has been removed", color=Color.green()).add_field(
                name="Strike count", value=strikes, inline=True).add_field(name="Reason", value=reason, inline=True)
            await channel.send(m.mention, embed=embed)

            await ctx.followup.send("Strike removed from {}".format(m))

    @slash(description="Main resignation command", guild_ids=[841671029066956831])
    async def resign(self, ctx: Interaction):
        pass

    @resign.subcommand(name="apply", description="Apply for resignation")
    async def _apply_(self, ctx: Interaction,
                      department=SlashOption(description="Department you are working in", required=True),
                      reason=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        db.execute(
            "INSERT OR IGNORE INTO resignData (user_id, accepted) VALUES (?, ?)", (ctx.user.id, 0))
        db.commit()

        channel = self.bot.get_channel(1002513633760260166)

        request = Embed(title="Resignation request of {} | {}".format(
            ctx.user, ctx.user.id), color=ctx.user.color)
        request.add_field(name="Department", value=department, inline=False)
        request.add_field(name="Reason of Resigning",
                          value=reason, inline=False)
        request.set_footer(
            text="To accept or deny the resignation, use `/resign approve USER_ID`")

        await ctx.followup.send("Your resignation has been requested")
        await channel.send(embed=request)

    @resign.subcommand(name="approve", description="Approve a resignation")
    @has_any_role(core_team, chr, coo)
    async def __approve__(self, ctx: Interaction, member: Member = SlashOption(required=True),
                          department=SlashOption(required=True), kick=SlashOption(
                description="Only use it if the member is planning on a full resignation (leaving the staff team)",
                choices=["True", "False"], required=False)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672222136991757)
        data = db.execute(
            "SELECT * FROM resignData WHERE user_id = ?", (member.id,)).fetchone()

        if data == None:
            await ctx.followup.send("Invalid User ID")

        elif data[0] == ctx.user.id:
            await ctx.followup.send("You can't approve your own resignation")

        elif member.top_role >= ctx.user.top_role:
            await ctx.followup.send("You cannot approve a resignation from someone who has a higher role than you")

        else:
            db.execute(
                "UPDATE resignData SET accepted = ? WHERE user_id = ?", (1, member.id,))
            db.commit()

            if kick == "True":
                try:
                    try:
                        await member.send("Your resignation has been approved. Thank you for working with us.")
                    except:
                        pass
                    await member.kick(reason="Resigned from LOA Staff")
                    await channel.send("{} has left the Staff Team".format(member))

                except:
                    await ctx.followup.send(
                        "{} couldn't be kicked out due to role hierarchy. Please do it manually if you can")
                    await channel.send("{} has left the Staff Team. Thank you for working with us".format(member))

            elif kick == None:
                await channel.send("{} has resigned from {}".format(member.mention, department))

            elif kick == "False":
                await channel.send("{} has resigned from {}".format(member.mention, department))

        await ctx.followup.send("Accepted resignation of {}".format(member))

    @strike.subcommand(description="Appeal your strike")
    async def appeal(self, ctx: Interaction,
                     strike_id=SlashOption(description="Enter the strike ID here", required=True),
                     department=SlashOption(choices=["Management", "Human Resources", "Moderation", "Marketing"])):
        view = Start_Appeal(self.bot, strike_id, department)
        msg = """
Before you start appealing your strike, please make sure:
    1. Your reason is valid and accurate
    2. You have proof in media links if necessary
        
If you feel it meets those conditions, click the button below.
Also just to let you know, your user ID is logged when doing this application so if you troll, we will take actions."""

        await ctx.send(msg, view=view, ephemeral=True)

    @strike.subcommand(description="Approve or deny a strike")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def verdict(self, ctx: Interaction, strike_appeal_id=SlashOption(required=True),
                      department=SlashOption(choices=["Management", "Human Resources", "Moderation", "Marketing"],
                                             required=True),
                      verdict=SlashOption(choices=["accept", "deny"], required=True)):
        await ctx.response.defer()
        channel = self.bot.get_channel(841672405444591657)
        user = fetch_striked_staff(strike_appeal_id, department)

        if user == None:
            await ctx.followup.send("Invalid Strike Appeal ID passed", delete_after=5)

        elif user[0] != department:
            await ctx.followup.send("Invalid department entered", delete_after=5)

        else:
            if verdict == "accept":
                revoke_strike(department, user[2])

                strikes = get_strikes(department, user[1])

                staff_member = ctx.guild.get_member(user[1])
                msg = "{}, your appeal for your strike has been appealled. You now have {} strikes".format(
                    staff_member.mention, len(strikes))

            elif verdict == "deny":
                staff_member = ctx.guild.get_member(user[1])
                msg = "{}, your appeal for your strike has been denied.".format(
                    staff_member.mention)

            db.commit()

            if ctx.channel.id == 841672405444591657:
                await ctx.send(msg)

            else:
                await channel.send(msg)
                await ctx.followup.send("Verdict given to appeal")

    @slash(description="Main pricelist command", guild_ids=[841671029066956831])
    async def pricelist(self, ctx: Interaction):
        pass

    @pricelist.subcommand(description="Get a list of LOA coin pricelist")
    async def loacoins(self, ctx:Interaction):
        await ctx.response.defer()
        thread_cat:CategoryChannel = self.bot.get_channel(862275910165594142)
        
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                shouts=Embed(color=Color.blue())
                shouts.title= "Shoutouts & Custom Channels"
                shouts.description="""
Normal Shoutout ( Without Pings ) : 400

Add-ons:
- Shoutout Ping : 50
- Partner Ping : 30
- Others Ping: 20


Normal Custom Channels ( Without Pings, last for 7 days ) : 800

Add-ons:
- Shoutout Ping : 100
- Partner Ping: 60
- Others Ping: 40
- Real Custom Channel ( You may put anything you want in the channel at anytime, but no more roles will be pinged and the content must fit the <#705956109592035389> ) : 350
- Per day after the first 7 days: 100
"""

                giveads = Embed(color=Color.blue())
                giveads.title = "Giveaways & Auto Advertisements"
                giveads.description = """
Normal Giveaway ( With Giveaway Ping & Requires to join your server, lasts for 1 day ) : 1000

Add-ons:
- Dedicated Channel: 800
- Prize provided by your server : 0
- Prize in our server : 50 per person
- Each winner (originally one winner) : 10
- Each day (duration of the giveaway, 1 day is given originally) : 10

Normal Auto Advertisements ( Every 8 hours ) for 7 days in <#757476260690657281> : 600

Add-ons:
- Every 4 hours : 100
- Every 2 hours : 200
- Every 30 minutes : 400
- Each channel of your choice : 300 
"""

                memberships = Embed(color=Color.blue())
                memberships.title = "Memberships"
                memberships.description = """
LOA Premium Membership
- 30 days: 3000 LOA Coins
- 365 (a year): 30000 LOA Coins ( ⭐ saving 6000 LOA Coins)

What is included in Premium Membership:
- Premium Role in Lead of Advertising
- Access to <#716897785961775165>
- Monthly Shoutout (DM <@!710733052699213844> to claim at the 1st day of each month)
- Access to VIP Lounge

LOA Executive Membership
- 30 days: 8000 LOA Coins
- 365 (a year): 80000 LOA Cions (⭐ saving 16000 LOA Coins)

What is included in Executive Membership:
- All above perks
- Bonus entries when joining giveaways
- VIP role in all <#941117023914713148> servers (if have^)
- Access to all <#941117023914713148> servers VIP Lounge (if have^)
- 5 shoutouts for free for each month (each shoutout must be claimed after 24 hours of the previous shoutout claiming time)
- 20% off per each <#869201807828725790> purchasement

^ = Available in Lead of Advertising, LOA Safety Centre and Lead of Gaming
"""

                openads = Embed(color=Color.blue())
                openads.title = "Open Network Auto Advertisement"
                openads.description = """
Auto Advertisement for 7 days - 50000

Add-ons:
- Every 4 hours: 0 (default)
- Every 1 hour: 500
- Server advertisement less than 50 characters: 200
- Per day after default: 400 
"""

                special = Embed(color=Color.blue())
                special.title = "Open Network Auto Advertisement"
                special.description = """
Custom channel under <#707117465049759744> category:
- 1 day: 10000
- per day after that one day: 8000

Custom Channel on the top of the server:
- 1 day: 15000
- per day after that one day: 12500

<#959811761282891856> with Job Announcement Ping:
- per announcement: 5000
- Default stay for 1 day, after default stay time per day: 1000  
"""

                embeds=[shouts, giveads, memberships, openads, special]
                await ctx.followup.send(embeds=embeds)

    @pricelist.subcommand(description="Get a list of LOA coin pricelist")
    async def paidplans(self, ctx: Interaction):
        await ctx.response.defer()
        thread_cat: CategoryChannel = self.bot.get_channel(862275910165594142)
        for channel in thread_cat.channels:
            if ctx.channel.id == channel.id:
                embed=Embed(color=Color.blue())
                embed.title="Paid plans"
                embed.description="""
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

                await ctx.followup.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(staff_mngm(bot))
