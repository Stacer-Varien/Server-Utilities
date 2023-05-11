from datetime import date, datetime, timedelta
import os
from discord import Guild, Interaction, Member, TextChannel, User
from assets.not_allowed import no_invites, no_pings
from config import db
from typing import Optional
from discord.ext.commands import Bot
from tabulate import tabulate


class Appeal:
    def __init__(self, user: User, appeal_id: int):
        self.user = user
        self.appeal_id = appeal_id

    def check(self):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ? AND appeal_id = ?",
            (
                self.user.id,
                self.appeal_id,
            ),
        ).fetchone()
        if data == None:
            return None
        else:
            return data

    def remove(self):
        db.execute(
            "DELETE FROM warnData WHERE appeal_id = ? AND user_id = ?",
            (
                self.appeal_id,
                self.user.id,
            ),
        )
        db.execute(
            "UPDATE warnDATA_v2 SET warn_point = warn_point - ? WHERE user_id = ?",
            (
                1,
                self.user.id,
            ),
        )
        db.commit()


class LOAWarn:
    def __init__(self, user: User, moderator: User = None, warn_id: int = None) -> None:
        self.user = user
        self.moderator = moderator
        self.warn_id = warn_id
        self.today = date.today()
        self.monday = self.today - timedelta(days=self.today.weekday())
        self.sunday = self.monday + timedelta(days=6)

    def prior_week_end(self):
        return datetime.today() + timedelta(
            days=((datetime.today().isoweekday() + 6) % 7)
        )

    def prior_week_start(self):
        return self.prior_week_end() - timedelta(days=6)

    def check(self):
        data = db.execute(
            "SELECT * FROM loaAdwarnData WHERE user_id = ? AND warn_id = ?",
            (
                self.user.id,
                self.warn_id,
            ),
        ).fetchone()
        db.commit()

        if data == None:
            return None

        else:
            return data

    def give(self, channel: TextChannel, reason: str):
        data = db.execute(
            "SELECT * FROM loaAdwarnData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        data2 = db.execute(
            "SELECT * FROM loaAdwarnData_v2 WHERE user_id= ?", (self.user.id,)
        ).fetchone()
        db.commit()
        start = self.prior_week_start().strftime("%d%m%Y")
        end = self.prior_week_end().strftime("%d%m%Y")
        current_time = datetime.now()
        next_warn = current_time + timedelta(minutes=45)
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO loaAdwarnData (user_id, reason, warn_id, mod_id) VALUES (?,?,?,?)",
                (
                    self.user.id,
                    "{} - {}".format(channel.mention, reason),
                    self.warn_id,
                    self.moderator.id,
                ),
            )
            db.commit()

            db.execute(
                "INSERT OR IGNORE INTO loaAdwarnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                (
                    self.user.id,
                    1,
                    round(next_warn.timestamp()),
                ),
            )
            db.commit()

            db.execute(
                "INSERT OR IGNORE INTO LOAwarnData_v3 (mod_id, points, start, end) VALUES (?,?,?,?)",
                (
                    self.moderator.id,
                    1,
                    start,
                    end,
                ),
            )
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute(
                "UPDATE loaAdwarnData_v2 SET warn_point = warn_point + ? WHERE user_id = ?",
                (
                    1,
                    self.user.id,
                ),
            )
            db.commit()

            db.execute(
                "UPDATE loaAdwarnData_v2 SET time = ? WHERE user_id = ?",
                (
                    round(next_warn.timestamp()),
                    self.user.id,
                ),
            )
            db.commit()

            db.execute(
                "UPDATE LOAwarnData_v3 SET points = points + ? WHERE mod_id = ?",
                (
                    1,
                    self.moderator.id,
                ),
            )
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False

    def get_points(self) -> int:
        try:
            warnpointdata = db.execute(
                "SELECT warn_point FROM loaAdwarnData_v2 WHERE user_id = ?",
                (self.user.id,),
            ).fetchone()
            db.commit()
            return warnpointdata[0]
        except:
            return 0

    def remove(self):
        data = self.check()
        db.execute(
            "DELETE FROM loaAdwarnData WHERE warn_id = ? and user_id = ?",
            (
                self.warn_id,
                self.user.id,
            ),
        )
        db.commit()
        db.execute(
            "UPDATE loaAdwarnData_v2 SET warn_point = warn_point - ? WHERE user_id = ?",
            (
                1,
                self.user.id,
            ),
        )
        db.commit()
        db.execute(
            "UPDATE LOAwarnData_v3 SET points = points - ? WHERE mod_id = ?",
            (1, int(data[3])),
        )
        db.commit()

        if self.get_points() == 0:
            db.execute(
                "DELETE FROM loaAdwarnData_v2 WHERE user_id = ?", (self.user.id,)
            )
            db.commit()

    def get_time(self) -> int:
        timedata = db.execute(
            "SELECT time FROM loaAdwarnData_v2 WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return timedata[0]


class LOAMod:
    def __init__(self, mod: Optional[User] = None) -> None:
        self.mod = mod
        self.today = date.today()
        self.monday = self.today - timedelta(days=self.today.weekday())
        self.sunday = self.monday + timedelta(days=6)

    def update_week(self):
        start = int(self.monday.strftime("%d%m%Y"))
        end = int(self.sunday.strftime("%d%m%Y"))
        data = db.execute(
            "INSERT OR IGNORE INTO LOAwarnData_v3 (mod_id, points, start, end) VALUES (?,?,?,?)",
            (
                self.mod.id,
                1,
                start,
                end,
            ),
        )
        if data.rowcount == 0:
            db.execute(
                "UPDATE LOAwarnData_v3 SET points = points + ? WHERE mod_id = ?",
                (
                    1,
                    self.mod.id,
                ),
            )
        db.commit()

    def reset_week(self):
        start = int(self.monday.strftime("%d%m%Y"))
        end = int(self.sunday.strftime("%d%m%Y"))

        if int(self.today.strftime("%d%m%Y")) == end:
            db.execute(
                "DELETE FROM LOAwarnData_v3 WHERE start = ? AND end = ?",
                (
                    start,
                    end,
                ),
            )
            db.commit()
        else:
            return False

    async def checks(self, bot: Bot):
        data = db.execute("SELECT * FROM LOAwarnData_v3").fetchall()
        mods = []
        for i in data:
            mod = await bot.fetch_user(int(i[0]))
            points = i[1]
            mods.append([str(mod), str(points)])

        col_names = ["Moderator", "Points"]
        return tabulate(mods, headers=col_names, tablefmt="pretty")


class Warn:
    def __init__(self, user: User, moderator: User = None, warn_id: int = None) -> None:
        self.user = user
        self.moderator = moderator
        self.warn_id = warn_id

    def check(self):
        data = db.execute(
            "SELECT * FROM warnDATA WHERE user_id = ? AND warn_id = ?",
            (
                self.user.id,
                self.warn_id,
            ),
        ).fetchone()
        db.commit()

        if data == None:
            return None

        else:
            return data

    def auto_give(self, channel: TextChannel, appeal_id: int):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        data2 = db.execute(
            "SELECT * FROM warnData_v2 WHERE user_id= ?", (self.user.id,)
        ).fetchone()
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
                ),
            )

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
                ),
            )
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False

    def give(self, channel: TextChannel, reason: str):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        data2 = db.execute(
            "SELECT * FROM warnData_v2 WHERE user_id= ?", (self.user.id,)
        ).fetchone()
        db.commit()
        current_time = datetime.now()
        next_warn = current_time + timedelta(hours=1)
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id) VALUES (?,?,?,?)",
                (
                    self.user.id,
                    self.moderator.id,
                    "{} - {}".format(channel.mention, reason),
                    self.warn_id,
                ),
            )

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
                ),
            )
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False

    def get_points(self) -> int:
        try:
            warnpointdata = db.execute(
                "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (self.user.id,)
            ).fetchone()
            db.commit()
            return warnpointdata[0]
        except:
            return 1

    def get_time(self) -> int:
        timedata = db.execute(
            "SELECT time FROM warnData_v2 WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return timedata[0]


def check_illegal_invites(message, channel: int):
    if "discord.gg" in message:
        if channel in no_invites:
            return True
        else:
            return False


def check_illegal_mentions(message, channel: int):
    pings = ["@everyone", "@here"]
    if any(word in message for word in pings):
        if channel in no_pings:
            return True
        else:
            return False


class Strike:
    def __init__(
        self, department: Optional[str] = None, member: Optional[User] = None
    ) -> None:
        self.department = department
        self.member = member

    def give(self):
        data = db.execute(
            "INSERT OR IGNORE INTO strikeData (department, user_id, count) VALUES (?,?,?)",
            (
                self.department,
                self.member.id,
                1,
            ),
        )
        if data.rowcount == 0:
            db.execute(
                "UPDATE strikeData SET count = count + ? WHERE department = ? AND user_id = ?",
                (
                    1,
                    self.department,
                    self.member.id,
                ),
            )
        db.commit()

    def counts(self):
        data = db.execute(
            "SELECT * FROM strikeData WHERE department = ? AND user_id = ?",
            (
                self.department,
                self.member.id,
            ),
        ).fetchall()

        if data == None:
            return 0
        else:
            return len(data)

    def check(self):
        data = db.execute(
            "SELECT * FROM strikeData WHERE user_id = ? AND department = ?",
            (
                self.member.id,
                self.department,
            ),
        ).fetchone()

        if data == None:
            return None
        else:
            return data

    def revoke(self):
        db.execute(
            "UPDATE strikeData SET count = count - ? WHERE user_id = ? and department = ?",
            (
                1,
                self.member.id,
                self.department,
            ),
        )
        db.commit()
        if self.counts() == 0:
            db.execute(
                "DELETE FROM strikeData WHERE user_id = ? AND department = ?",
                (
                    self.member.id,
                    self.department,
                ),
            )
            db.commit()


class Partner:
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

    async def approve(self, ctx: Interaction):
        if self.server.id == 740584420645535775:
            with open("partnerships/orleans/{}.txt".format(self.user.id), "r") as f:
                content = "".join(f.readlines())
            os.remove("partnerships/orleans/{}.txt".format(self.user.id))
            partner_role = self.server.get_role(1051047558224543844)
            if partner_role in self.user.roles:
                pass
            else:
                await self.user.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(1040380792406298645)
            await partner_channnel.send(content=content)
        elif self.server.id == 925790259160166460:
            with open("partnerships/hazeads/{}.txt".format(self.user.id), "r") as f:
                content = "".join(f.readlines())
            os.remove("partnerships/hazeads/{}.txt".format(self.user.id))
            partner_role = self.server.get_role(950354444669841428)
            if partner_role in self.user.roles:
                pass
            else:
                await self.user.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(1040380792406298645)
            await partner_channnel.send(content=content)
        return await ctx.followup.send("Partnership approved")

    async def deny(self, ctx: Interaction, reason: str):
        if self.server.id == 740584420645535775:
            os.remove("partnerships/orleans/{}.txt".format(self.user.id))
        elif self.server.id == 925790259160166460:
            os.remove("partnerships/hazeads/{}.txt".format(self.user.id))

        try:
            await self.user.send(
                f"Your partnership request was denied because:\n{reason}"
            )
            msg = "Partnership denied and reason sent"
        except:
            msg = "Partnership denied"
        return await ctx.followup.send(msg)


class Break:
    def __init__(self, member: Optional[User] = None) -> None:
        self.member = member

    def check_breaks(self):
        data = db.execute("SELECT * FROM breakData WHERE accepted = ?", (1,)).fetchall()
        db.commit()
        return data

    def remove(self):
        db.execute("DELETE FROM breakData WHERE user_id = ?", (self.member.id,))
        db.commit()

    def add_request(
        self,
        server: int,
        duration: str,
        reason: str,
        accepted: int,
        start: int,
        ends: int,
    ):
        db.execute(
            "INSERT OR IGNORE INTO breakData (user_id, guild_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?)",
            (
                self.member.id,
                server,
                duration,
                reason,
                accepted,
                start,
                ends,
            ),
        )
        db.commit()

    def check(self, server: int):
        data = db.execute(
            "SELECT * FROM breakData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                server,
            ),
        ).fetchone()
        if data == None:
            return None
        else:
            return data

    def approve(self, server: int, start: int, ends: int):
        db.execute(
            "UPDATE breakData SET accepted = ? WHERE user_id = ? and guild_id = ?",
            (
                1,
                self.member.id,
                server,
            ),
        )
        db.execute(
            "UPDATE breakData SET start = ? WHERE user_id = ? and guild_id = ?",
            (
                start,
                self.member.id,
                server,
            ),
        )
        db.execute(
            "UPDATE breakData SET ends = ? WHERE user_id = ? and guild_id = ?",
            (
                ends,
                self.member.id,
                server,
            ),
        )
        db.commit()

    def deny(self, server: int):
        db.execute(
            "DELETE FROM breakData WHERE user_id = ? and guild_id = ?",
            (
                self.member.id,
                server,
            ),
        )
        db.commit()

    def end(self, server: int):
        db.execute(
            "DELETE FROM breakData WHERE user_id = ? and guild_id = ?",
            (
                self.member.id,
                server,
            ),
        )
        db.commit()


class Resign:
    def __init__(self, member: User):
        self.member = member

    def apply(self):
        db.execute(
            "INSERT OR IGNORE INTO resignData (user_id, accepted) VALUES (?, ?)",
            (
                self.member.id,
                0,
            ),
        )
        db.commit()

    def check(self):
        data = db.execute(
            "SELECT * FROM resignData WHERE user_id = ?", (self.member.id,)
        ).fetchone()
        db.commit()

        if data == None:
            return None
        else:
            return data

    def approve(self):
        db.execute(
            "UPDATE resignData SET accepted = ? WHERE user_id = ?",
            (
                1,
                self.member.id,
            ),
        )
        db.commit()

    def deny(self):
        db.execute("DELETE FROM resignData WHERE user_id = ?", (self.member.id,))
        db.commit()


class Plans:
    def __init__(self, server: int):
        self.server = server

    def add(self, user: User, until: int, plan: str, claimee: User, plan_id: int):
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
            ),
        )
        db.commit()

    def get(self, plan_id: int):
        data = db.execute(
            "SELECT * FROM planData WHERE plan_id = ? AND server_id = ?",
            (
                plan_id,
                self.server,
            ),
        ).fetchone()

        if data == None:
            return None
        else:
            return data

    def check(self):
        data = db.execute(
            "SELECT * FROM planData where server_id = ?", (self.server,)
        ).fetchall()
        db.commit()
        return data

    def remove(self, buyer: User, plan_id: int):
        db.execute(
            "DELETE FROM planData WHERE user_id = ? AND plan_id= ? AND server_id= ?",
            (
                buyer.id,
                plan_id,
                self.server,
            ),
        )
        db.commit()
