from datetime import *
import os
from discord import *
from assets.not_allowed import no_invites, no_pings
from discord.ext.commands import Bot
from config import db
from typing import Optional


def convert_loop_time(time: float):
    """Convert a float from humanfriendly.parse_timespan to loop times for the autoad maker"""
    if time < 60:
        return f"seconds={time}"
    elif time < 3600:
        return f"minutes={time/60}"
    elif time < 86400 or time >= 86400:
        return f"hours={time/3600}"


class Appeal():

    def __init__(self, appeal_id: int):
        self.user = user
        self.appeal_id = appeal_id

    def check_appeal(self):
        data = db.execute("SELECT * FROM warnData WHERE appeal_id = ?",
                          (self.appeal_id, )).fetchone()
        if data == None:
            return None
        else:
            return data

    def remove_warn(self, member_id: int):
        db.execute("DELETE FROM warnData WHERE appeal_id = ?",
                   (self.appeal_id, ))
        db.execute(
            "UPDATE warnDATA_v2 SET warn_point = warn_point - ? where user_id = ?",
            (
                1,
                member_id,
            ))
        db.commit()


class Warn():

    def __init__(self,
                 user: Member,
                 moderator: Member,
                 warn_id: int = None) -> None:
        self.user = user
        self.moderator = moderator
        self.warn_id = warn_id

    def check_warn(self):
        data = db.execute(
            "SELECT * FROM warnDATA WHERE user_id = ? AND warn_id = ?", (
                self.user.id,
                self.warn_id,
            )).fetchone()
        db.commit()

        if data == None:
            return None

        else:
            data = db.execute("SELECT * FROM warnDATA WHERE user_id = ?",
                              (self.user.id, ))
            db.commit()
            return data

    def give_adwarn_auto(self, channel: TextChannel, appeal_id: int):
        data = db.execute("SELECT * FROM warnData WHERE user_id = ?",
                          (self.user.id, )).fetchone()
        data2 = db.execute("SELECT * FROM warnData_v2 WHERE user_id= ?",
                           (self.user.id, )).fetchone()
        db.commit()
        current_time = datetime.now()
        next_warn = current_time + timedelta(hours=1)

        reason = f"Incorrectly advertising in {channel.mention}"
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (
                    self.user.id,
                    self.moderator.id,
                    reason,
                    self.warn_id,
                    appeal_id,
                ))

            db.execute(
                "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                (self.user.id, 1, round(next_warn.timestamp())),
            )
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute(
                "UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?",
                (
                    1,
                    round(next_warn.timestamp()),
                    self.user.id,
                ))
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False

    def give_adwarn(self, channel: TextChannel, reason: str, appeal_id: int):
        data = db.execute("SELECT * FROM warnData WHERE user_id = ?",
                          (member, )).fetchone()
        data2 = db.execute("SELECT * FROM warnData_v2 WHERE user_id= ?",
                           (member, )).fetchone()
        db.commit()
        current_time = datetime.now()
        next_warn = current_time + timedelta(hours=1)
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (
                    self.user.id,
                    self.moderator.id,
                    '{} - {}'.format(channel.mention, reason),
                    self.warn_id,
                    appeal_id,
                ))

            db.execute(
                "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                (member, 1, round(next_warn.timestamp())))
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute(
                "UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?",
                (
                    1,
                    round(next_warn.timestamp()),
                    self.user.id,
                ))
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False

    def get_warn_points(self) -> int:
        try:
            warnpointdata = db.execute(
                "SELECT warn_point FROM warnData_v2 WHERE user_id = ?",
                (self.user.id, )).fetchone()
            db.commit()
            return warnpointdata[0]
        except:
            return 1

    def get_warn_id(self):
        data = db.execute("SELECT warn_id FROM warnData WHERE user_id = ?",
                          (self.user.id, )).fetchone()
        return data[0]


def check_illegal_invites(message, channel: int):
    if 'discord.gg' in message:
        if channel in no_invites:
            return True
        else:
            return False


def check_illegal_mentions(message, channel: int):
    pings = ['@everyone', '@here']
    if any(word in message for word in pings):
        if channel in no_pings:
            return True
        else:
            return False


class Strike():

    def __init__(self,
                 department: Optional[str] = None,
                 member: Optional[Member] = None) -> None:
        self.department = department
        self.member = member

    def give(self, strike_id: int, appeal_id: int):
        db.execute(
            "INSERT OR IGNORE INTO strikeData (department, user_id, strike_id, appeal_id) VALUES (?,?,?,?)",
            (
                self.department,
                self.member.id,
                strike_id,
                appeal_id,
            ))
        db.commit()

    def get_strikes(self):
        data = db.execute(
            "SELECT * FROM strikeData WHERE department = ? AND user_id = ?", (
                self.department,
                self.member.id,
            )).fetchall()

        if data == None:
            return None
        else:
            return len(data)

    def check_id(self, strike_id: int):
        data = db.execute(
            "SELECT * FROM strikeData WHERE strike_id = ? AND department = ?",
            (
                strike_id,
                self.department,
            )).fetchone()

        if data == None:
            return None
        else:
            return data

    def revoke(self, strike_id: int):
        db.execute(
            "DELETE FROM strikeData WHERE strike_id = ? AND department = ?",
            (strike_id, self.department))
        db.commit()

    def get_appeal_id(self, strike_id: int):
        data = db.execute(
            "SELECT appeal_id FROM strikeData WHERE strike_id = ? AND department = ?",
            (strike_id, self.department)).fetchone()
        db.commit()
        return data[0]

    def fetch_striked_staff(self, appeal_id: int):
        data = db.execute(
            "SELECT * FROM strikeData WHERE appeal_id = ? AND department = ?",
            (
                appeal_id,
                self.department,
            )).fetchone()
        db.commit()

        if data == None:
            return None
        else:
            return data


class Partner():

    def __init__(self, user: Member, server: Guild):
        self.user = user
        self.server = server

    def check(self):
        if self.server.id == 740584420645535775:
            path = "/partnerships/orleans/{}.txt".format(self.user.id)
            check = os.path.exists(path)
            if check == True:
                return True
            else:
                return None

        elif self.server.id == 925790259160166460:
            path = "/partnerships/hazeads/{}.txt".format(self.user.id)
            check = os.path.exists(path)
            if check == True:
                return True
            else:
                return None

    async def approve(self, ctx:Interaction):
        if self.server.id == 740584420645535775:
            with open("partnerships/orleans/{}.txt".format(self.user.id),
                      'r') as f:
                content = "".join(f.readlines())
            os.remove("partnerships/orleans/{}.txt".format(self.user.id))
            partner_role = self.server.get_role(1051047558224543844)
            if partner_role in self.user.roles:
                pass
            else:
                await self.user.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(
                1040380792406298645)
            await partner_channnel.send(content=content)
        elif self.server.id == 925790259160166460:
            with open("partnerships/hazeads/{}.txt".format(self.user.id),
                      'r') as f:
                content = "".join(f.readlines())
            os.remove("partnerships/hazeads/{}.txt".format(self.user.id))
            partner_role = self.server.get_role(950354444669841428)
            if partner_role in self.user.roles:
                pass
            else:
                await self.user.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(
                1040380792406298645)
            await partner_channnel.send(content=content)
        return await ctx.followup.send("Partnership approved")

    async def deny(self, ctx:Interaction, reason: str):
        if self.server.id == 740584420645535775:
            os.remove("partnerships/orleans/{}.txt".format(self.user.id))
        elif self.server.id == 925790259160166460:
            os.remove("partnerships/hazeads/{}.txt".format(self.user.id))

        try:
            await self.user.send(
                f"Your partnership request was denied because:\n{reason}")
            msg="Partnership denied and reason sent"
        except:
            msg= "Partnership denied"
        return await ctx.followup.send(msg)


class Break():

    def __init__(self, member: Optional[Member] = None) -> None:
        self.member = member

    def check_loa_breaks(self):
        data = db.execute("SELECT * FROM breakData WHERE accepted = ?",
                          (1, )).fetchall()
        db.commit()
        return data

    def remove_loa_break(self):
        db.execute("DELETE FROM breakData WHERE user_id = ?",
                   (self.member.id, ))
        db.commit()

    def add_break_request(self, server: int, break_id: int, duration: str,
                          reason: str, accepted: int, start: int, ends: int):
        db.execute(
            "INSERT OR IGNORE INTO breakData (user_id, guild_id, break_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?,?)",
            (
                self.member.id,
                server,
                break_id,
                duration,
                reason,
                accepted,
                start,
                ends,
            ))
        db.commit()

    def fetch_break_id(break_id: int, server: int):
        data = db.execute(
            "SELECT * FROM breakData WHERE break_id = ? AND guild_id = ?", (
                break_id,
                server,
            )).fetchone()
        if data == None:
            return None
        else:
            return data

    def approve_break(self, server: int, start: int, ends: int):
        db.execute(
            "UPDATE breakData SET accepted = ? WHERE user_id = ? and guild_id = ?",
            (
                1,
                self.member.id,
                server,
            ))
        db.execute(
            "UPDATE breakData SET start = ? WHERE user_id = ? and guild_id = ?",
            (
                start,
                self.member.id,
                server,
            ))
        db.execute(
            "UPDATE breakData SET ends = ? WHERE user_id = ? and guild_id = ?",
            (
                ends,
                self.member.id,
                server,
            ))
        db.commit()

    def deny_break(break_id: int, server: int):
        db.execute("DELETE FROM breakData WHERE break_id = ? and guild_id = ?",
                   (
                       break_id,
                       server,
                   ))
        db.commit()

    def end_break(self, server: int):
        db.execute("DELETE FROM breakData WHERE user_id = ? and guild_id = ?",
                   (
                       self.member.id,
                       server,
                   ))
        db.commit()


class Resign():

    def __init__(self, member: Member):
        self.member = member

    def resign_apply(self):
        db.execute(
            "INSERT OR IGNORE INTO resignData (user_id, accepted) VALUES (?, ?)",
            (self.user.id, 0))
        db.commit()

    def check_resign(self):
        data = db.execute("SELECT * FROM resignData WHERE user_id = ?",
                          (self.member.id, )).fetchone()
        db.commit()

        if data == None:
            return None
        else:
            return data

    def approve_resign(self):
        db.execute("UPDATE resignData SET accepted = ? WHERE user_id = ?", (
            1,
            self.member.id,
        ))
        db.commit()

    def deny_resign(self):
        db.execute("DELETE FROM resignData WHERE WHERE user_id = ?",
                   (self.member.id, ))
        db.commit()


class Plans():

    def __init__(self, server: int):
        self.server = server

    def add_plan(self, user: User, until: int, plan: str, claimee: User,
                 plan_id: int):
        db.execute(
            "INSERT OR IGNORE INTO planData (user_id, started, until, plans, set_by, plan_id, server_id) VALUES (?,?,?,?,?,?,?)",
            (
                user.id,
                round(datetime.now().timestamp()),
                until,
                plan,
                claimee.id,
                plan_id,
                self.server,
            ))
        db.commit()

    def get_plan(self, plan_id: int):
        data = db.execute(
            "SELECT * FROM planData WHERE plan_id = ? AND server_id = ?", (
                plan_id,
                self.server,
            )).fetchone()

        if data == None:
            return None
        else:
            return data

    def check_plans(self):
        data = db.execute("SELECT * FROM planData where server_id = ?",
                          (self.server, )).fetchall()
        db.commit()
        return data

    def remove_plan(self, plan_id: int):
        db.execute('DELETE FROM planData WHERE plan_id= ? AND server_id= ?', (
            plan_id,
            self.server,
        ))
        db.commit()

class AutoAd():
    def __init__(self, bot:Bot, server:Guild):
        self.bot=bot
        self.server=server
    
    async def check_channel(self, channels:str):
        if self.server.id==841671029066956831:
            server= await self.bot.fetch_guild(841671029066956831)
        elif self.server.id==925790259160166460:
            server= await self.bot.fetch_guild(925790259160166460)            
        try:
            for channel in channels:
                await server.fetch_channel(int(channel))
        except:
            return None

          
