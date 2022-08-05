from datetime import datetime, timedelta
from random import randint

from humanfriendly import parse_timespan
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import has_any_role
from nextcord.ext.commands import Cog

from assets.confirm_buttoms import Confirmation
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
    def __init__(self, bot):
        self.bot = bot

    @slash(description="Fire staff from HAZE Advertising", guild_ids=[925790259160166460])
    @has_any_role(ha_admin, ha_hr)
    async def fire_ha_staff(self, ctx: Interaction, member: Member = SlashOption(required=True),
                            role: Role = SlashOption(required=True), reason=SlashOption(required=True)):
        await ctx.response.defer()
        if member == ctx.user:
            await ctx.followup.send("You can't fire yourself...")

        elif member.top_role >= ctx.user.top_role:
            await ctx.followup.send("You can't fire someone who has a higher role than you...")

        else:
            await member.remove_roles(role, reason=reason)
            channel = self.bot.get_channel(925790262104580104)
            await channel.send("{} was fired\nPosition: {}\nReason: {}".format(member, role.name, reason))

    @slash(description="Main staff break command", guild_ids=[841671029066956831])
    async def staff_break(self, ctx: Interaction):
        pass

    @staff_break.subcommand(description="Apply for break")
    async def apply(self, ctx: Interaction,
                    reason=SlashOption(description="Why do you want to go on break?", required=True),
                    duration_type=SlashOption(description="Is it timed or until further notice?",
                                              choices=["Timed (1h, 1h30m, etc)", "Until further notice"],
                                              required=True), duration=SlashOption(
                description="If you have selected the timed option, how long are you planning to take break?",
                required=False)):
        await ctx.response.defer()

        break_role = ctx.guild.get_role(841682795277713498)

        if break_role in ctx.user.roles:
            await ctx.followup.send("You are already on break")

        else:

            channel = await self.bot.fetch_channel(841676953613631499)
            break_id = randint(1, 99999)

            requested_break = Embed(title="New Break Request")
            requested_break.add_field(
                name="Staff Member", value=ctx.user, inline=False)
            requested_break.add_field(
                name="Role", value=ctx.user.top_role, inline=False)
            if duration_type == "Until further notice":
                duration = "Until further notice"
            else:
                a = datetime.now() + timedelta(seconds=parse_timespan(duration))
                b = round(a.timestamp())
                duration = "<t:{}:D>".format(b)
                requested_break.add_field(
                    name="Duration", value=duration, inline=False)
                requested_break.add_field(
                    name="Reason", value=reason, inline=False)
                requested_break.add_field(
                    name="Break ID", value=break_id, inline=False)
                requested_break.set_footer(
                    text="To approve or deny this request, use `/staff_break approve BREAK_ID` or `/staff_break deny BREAK_ID`")

                msg = await channel.send(embed=requested_break)
                await ctx.followup.send("Break successfully requested", delete_after=10.0)

                db.execute(
                    "INSERT OR IGNORE INTO breakData (user_id, guild_id, msg_id, break_id, duration, reason) VALUES (?,?,?,?,?,?)",
                    (ctx.user.id, ctx.guild.id, msg.id, break_id, duration, reason,))
                db.commit()

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
            accepted_break.add_field(
                name="Duration", value=data[4], inline=False)
            accepted_break.add_field(
                name="Reason", value=data[5], inline=False)
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

                db.execute(
                    "DELETE FROM breakData WHERE break_id = ? and guild_id = ?", (break_id, ctx.guild.id,))
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

            else:
                await ctx.followup.send("You are not on break. Please request for a break first.", delete_after=10.0)

    @slash(description="Main strike command", guild_ids=[841671029066956831])
    async def strike(self, ctx: Interaction):
        pass

    @strike.subcommand(description="Give a strike to a staff member for bad performance")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def give(self, ctx: Interaction, member: Member = SlashOption(required=True), department=SlashOption(
        choices=["Core Team", "Management", "Human Resources", "Moderation", "Marketing"], required=True),
                   reason=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)
        view = Confirmation()

        cur = db.execute(
            "INSERT OR IGNORE INTO strikeData (user_id, strikes, department) VALUES (?, ?, ?)",
            (member.id, 1, department,))

        if cur.rowcount == 0:
            db.execute("UPDATE strikeData SET strikes = strikes + ? WHERE user_id = ? AND department = ?",
                       (1, member.id, department,))

        db.commit()

        strikedata = db.execute(
            "SELECT strikes FROM strikeData WHERE user_id = ? AND department = ?", (member.id, department,)).fetchone()

        if strikedata == None:
            strikes = 1

        else:
            strikes = strikedata[0]

        if strikes == 3:
            await ctx.followup.send(
                f"{member} has reached the 3 strike quota. Should they be kicked out of this server?", view=view)
            await view.wait()

            if view.value == None:
                await ctx.edit_original_message("Timed out")

            elif view.value == True:
                await member.kick(reason="Staff member recieved 3 strikes")
                await ctx.edit_original_message("{} has been kicked due to recieving 3 strikes")
                await channel.send("{} has been kicked due to recieving 3 strikes")

            elif view.value == False:
                await ctx.edit_original_message("Kick cancelled. Might recommend firing them from the department")
                embed = Embed(title="You have been striked", color=Color.red()).add_field(name="Strike count",
                                                                                          value=strikes[0],
                                                                                          inline=True).add_field(
                    name="Department", value=department, inline=True).add_field(name="Reason", value=reason,
                                                                                inline=True)
                await channel.send(member.mention, embed=embed)
                await ctx.followup.send("Strike given to {}".format(member))
        else:
            embed = Embed(title="You have been striked", color=Color.red()).add_field(name="Strike count",
                                                                                      value=strikes,
                                                                                      inline=True).add_field(
                name="Department", value=department, inline=True).add_field(name="Reason", value=reason, inline=True)
            await channel.send(member.mention, embed=embed)
            await ctx.followup.send("Strike given to {}".format(member))

    @strike.subcommand(description="Remove a strike if a staff member has shown improvement")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def remove(self, ctx: Interaction, member: Member = SlashOption(required=True), department=SlashOption(
        choices=["Core Team", "Management", "Human Resources", "Moderation", "Marketing"], required=True),
                     reason=SlashOption(required=True)):
        await ctx.response.defer(ephemeral=True)
        channel = self.bot.get_channel(841672405444591657)

        data = db.execute("SELECT strikes FROM strikeData WHERE user_id = ? and department = ?",
                          (member.id, department,)).fetchone()

        if data == None:
            await ctx.followup.send("{} has no strikes in this department".format(member))

        else:

            db.execute(
                "UPDATE strikeData SET strikes = strikes - ? WHERE user_id = ? AND department = ?",
                (1, member.id, department,))
            db.commit()

            strikes = db.execute(
                "SELECT strikes FROM strikeData WHERE user_id = ? AND department = ?",
                (member.id, department,)).fetchone()

            if strikes[0] == 0:
                db.execute(
                    "DELETE FROM strikeData WHERE user_id = ? AND department = ?", (member.id, department,))
                db.commit()

                await ctx.followup.send("{}'s strike has been removed".format(member))

            embed = Embed(title="Your strike has been removed", color=Color.green()).add_field(
                name="Strike count", value=strikes[0], inline=True).add_field(name="Reason", value=reason, inline=True)
            await channel.send(member.mention, embed=embed)
            await ctx.followup.send("Strike given to {}".format(member))

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
    async def appeal(self, ctx: Interaction):
        view = Start_Appeal(self.bot)
        msg = """
        Before you start appealing your strike, please make sure:
        1. Your reason is valid and accurate
        2. You have proof in media links if necessary
        
        If you feel it meets those conditions, click the button below."""

        await ctx.send(msg, view=view)

    @strike.subcommand(description="Approve or deny a strike")
    @has_any_role(core_team, chr, coo, team_leader, staff_supervisor)
    async def verdict(self, ctx: Interaction, strike_appeal_id=SlashOption(required=True),
                      department=SlashOption(
                          choices=["Core Team", "Management", "Human Resources", "Moderation", "Marketing"],
                          required=True),
                      appealled=SlashOption(name="verdict?", choices=["accept", "deny"], required=True),
                      reason=SlashOption(required=False)):
        await ctx.response.defer()
        channel = self.bot.get_channel(841672405444591657)
        user = db.execute("SELECT * FROM strikeData WHERE strike_appeal_id = ? AND department = ?",
                          (strike_appeal_id, department,)).fetchone()

        if user == None:
            await ctx.followup.send("Invalid Strike Appeal ID passed", delete_after=5)

        elif user[2] != department:
            await ctx.followup.send("Invalid department entered", delete_after=5)

        else:
            if appealled == "accept":
                user_data = user[0]
                db.execute("DELETE FROM strike_appeal_data WHERE strike_appeal_id = ?, user_id = ? AND department = ?",
                           (strike_appeal_id, user_data, department,))
                db.execute("UPDATE strikeData SET strikes = strikes - ? WHERE user_id = ? AND ")

                strikes = db.execute("SELECT strikes FROM strikeData WHERE user_id = ? and department = ?",
                                     (user_data, department,))
                staff_member = ctx.guild.get_member(user_data)
                msg = "{}, your appeal for your strike has been appealled. You now have {} strikes".format(
                    staff_member.mention, strikes)

            elif appealled == "deny":
                user_data = user[0]
                db.execute("DELETE FROM strike_appeal_data WHERE strike_appeal_id = ?, user_id = ? AND department = ?",
                           (strike_appeal_id, user_data, department,))
                staff_member = ctx.guild.get_member(user_data)
                msg = "{}, your appeal for your strike has been denied."

            db.commit()

            if ctx.channel.id == 841672405444591657:
                await ctx.send(msg)

            else:
                await channel.send(msg)
                await ctx.followup.send("Verdict given to strike appeal")


def setup(bot):
    bot.add_cog(staff_mngm(bot))
