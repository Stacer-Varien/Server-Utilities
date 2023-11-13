import os
from datetime import date, datetime, timedelta
from typing import Literal, Optional

from discord import (
    Color,
    Embed,
    Guild,
    Interaction,
    Member,
    Message,
    TextChannel,
    User,
    Forbidden,
)
from discord.ext.commands import Bot
from tabulate import tabulate

from assets.not_allowed import no_invites, no_pings
from config import db


class Appeal:
    def __init__(self, user: Member, warn_id: int):
        self.user = user
        self.warn_id = warn_id

    def check(self):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ? AND warn_id = ?",
            (
                self.user.id,
                self.warn_id,
            ),
        ).fetchone()
        return data if data else None

    def remove(self):
        db.execute(
            "DELETE FROM warnData WHERE warn_id = ? AND user_id = ?",
            (
                self.warn_id,
                self.user.id,
            ),
        )
        db.commit()
        db.execute(
            "UPDATE warnDATA_v2 SET warn_point = warn_point - ? WHERE user_id = ?",
            (
                1,
                self.user.id,
            ),
        )
        db.commit()


class LOAWarn:
    def __init__(
        self, moderator: Optional[User] = None) -> None:
        self.moderator = moderator

    def check(self, user:Member,warn_id:int):
        data = db.execute(
            "SELECT * FROM loaAdwarnData WHERE user_id = ? AND warn_id = ?",
            (
                user.id,
                warn_id,
            ),
        ).fetchone()
        db.commit()

        return data if data else None

    @staticmethod
    def check_time(member: Member) ->(int|Literal[True]):
        data = db.execute(
            "SELECT time from loaAdwarnData_v2 WHERE user_id = ?", (member.id,)
        ).fetchone()
        db.commit()

        if (data == None) or (int(data[0]) <= round(datetime.now().timestamp())):
            return True
        return int(data[0])

    async def give(self, user:Member, channel: TextChannel, reason: str, warn_id:int) -> (Literal[False] | None):
        current_time = datetime.now()
        next_warn = current_time + timedelta(minutes=25)

        db.execute(
            "INSERT OR IGNORE INTO loaAdwarnData (user_id, reason, warn_id, mod_id) VALUES (?,?,?,?)",
            (
                user.id,
                "{} - {}".format(channel.mention, reason),
                warn_id,
                self.moderator.id,
            ),
        )
        db.commit()

        datav2 = db.execute(
            "INSERT OR IGNORE INTO loaAdwarnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
            (
                user.id,
                1,
                round(next_warn.timestamp()),
            ),
        )
        db.commit()

        if datav2.rowcount == 0:
            db.execute(
                "UPDATE loaAdwarnData_v2 SET warn_point = warn_point + ?, time = ? WHERE user_id = ?",
                (
                    1,
                    round(next_warn.timestamp()),
                    user.id,
                ),
            )
            db.commit()

        datav3 = db.execute(
            "INSERT OR IGNORE INTO LOAwarnData_v3 (mod_id, points) VALUES (?,?)",
            (
                self.moderator.id,
                1,
            ),
        )
        db.commit()

        if datav3.rowcount == 0:
            db.execute(
                "UPDATE LOAwarnData_v3 SET points = points + ? WHERE mod_id = ?",
                (
                    1,
                    self.moderator.id,
                ),
            )
            db.commit()

    def get_points(self) -> int:
        warnpointdata = db.execute(
            "SELECT warn_point FROM loaAdwarnData_v2 WHERE user_id = ?",
            (self.moderator.id,),
        ).fetchone()
        db.commit()
        return warnpointdata[0] if warnpointdata else 0

    def remove(self, user:Member, warn_id:int):
        mod_id = int(self.check()[3])
        db.execute(
            "DELETE FROM loaAdwarnData WHERE warn_id = ? AND user_id = ?",
            (
                warn_id,
                user.id,
            ),
        )
        db.commit()

        db.execute(
            "UPDATE loaAdwarnData_v2 SET warn_point = warn_point - ? WHERE user_id = ?",
            (
                1,
                user.id,
            ),
        )
        db.commit()

        db.execute(
            "UPDATE LOAwarnData_v3 SET points = points - ? WHERE mod_id = ?",
            (
                1,
                mod_id,
            ),
        )
        db.commit()

        if self.get_points() == 0:
            db.execute(
                "DELETE FROM loaAdwarnData_v2 WHERE user_id = ?",
                (user.id,),
            )
            db.commit()

    def delete(self, user:Member):
        if self.get_points() == 10:
            db.execute("DELETE FROM loaAdwarnData WHERE user_id = ?;", (user.id,))
            db.commit()
            db.execute(
                "DELETE FROM loaAdwarnData_v2 WHERE user_id = ?", (user.id,)
            )
            db.commit()


class LOAMod:
    def __init__(self, mod: Optional[User] = None) -> None:
        self.mod = mod
    
    @staticmethod
    def _cooldowns():
        data=db.execute("SELECT * FROM loaAdwarnData_v2 DESC").fetchall()
        db.commit()

        return data if data else None

    @staticmethod
    async def checks(bot: Bot):
        data = db.execute("SELECT * FROM LOAwarnData_v3 DESC").fetchall()
        db.commit()
        mods = []
        r = 0
        for i in data:
            mod = await bot.fetch_user(int(i[0]))
            points = i[1]
            r += 1
            mods.append(f"`{r}.` {mod.mention} - {points}\n")

        return "".join(mods)

    def add_mod_point(self):
        data = db.execute(
            "INSERT OR IGNORE INTO LOAwarnData_v3 (mod_id, points) VALUES (?,?)",
            (
                self.mod.id,
                1,
            )
        )
        db.commit()

        if data.rowcount == 0:
            db.execute(
                "UPDATE LOAwarnData_v3 SET points = points + ? WHERE mod_id = ?",
                (
                    1,
                    self.mod.id,
                )
            )
            db.commit()
    
    @staticmethod
    def reset_week():
        db.execute("DELETE FROM loaWarndata_v3;")
        db.commit()


class Warn:
    def __init__(
        self, user: Member, moderator: User = None, warn_id: int = None
    ) -> None:
        self.user = user
        self.moderator = moderator
        self.warn_id = warn_id

    def check(self):
        data = db.execute(
            "SELECT * FROM warnDATA WHERE user_id = ? AND warn_id = ?",
            (
                self.user.id,
                self.warn_id,
            )
        ).fetchone()
        db.commit()

        return data if data else None

    def auto_give(self, channel: TextChannel):
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
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id) VALUES (?,?,?,?)",
                (
                    self.user.id,
                    self.moderator.id,
                    reason,
                    self.warn_id,
                )
            )

            db.execute(
                "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                (
                    self.user.id,
                    1,
                    round(next_warn.timestamp()),
                ),
            )
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute(
                "UPDATE warnData_v2 SET warn_point = warn_point + ? WHERE user_id= ?",
                (
                    1,
                    self.user.id,
                ),
            )
            db.commit()

            db.execute(
                "UPDATE warnData_v2 SET time = ? WHERE user_id = ?",
                (
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
        if data is None:
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
                (
                    self.user.id,
                    1,
                    round(next_warn.timestamp()),
                ),
            )
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute(
                "UPDATE warnData_v2 SET warn_point = warn_point + ?, time = ? WHERE user_id = ?",
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
        warnpointdata = db.execute(
            "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        return warnpointdata[0] if warnpointdata else 0

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
        self, department: Optional[str] = None, member: Optional[Member] = None
    ) -> None:
        self.department = department
        self.member = member

    async def give(self):
        data = db.execute(
            "INSERT OR IGNORE INTO strikeData (department, user_id, count) VALUES (?, ?, 1)",
            (
                self.department,
                self.member.id,
            ),
        )
        db.commit()
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

    def counts(self) -> int:
        data = db.execute(
            "SELECT count FROM strikeData WHERE department = ? AND user_id = ?",
            (
                self.department,
                self.member.id,
            ),
        ).fetchone()
        db.commit()

        return int(data[0]) if data else 0

    def check(self):
        data = db.execute(
            "SELECT * FROM strikeData WHERE department = ? AND user_id = ?",
            (
                self.department,
                self.member.id,
            ),
        ).fetchone()

        return data if data else None

    async def revoke(self):
        db.execute(
            "UPDATE strikeData SET count = count - 1 WHERE department = ? AND user_id = ?",
            (
                self.department,
                self.member.id,
            ),
        )
        db.commit()

        if self.counts() == 0:
            db.execute(
                "DELETE FROM strikeData WHERE department = ? AND user_id = ?",
                (
                    self.department,
                    self.member.id,
                ),
            )
            db.commit()


class Partner:
    def __init__(self, user: Member, server: Guild):
        self.user = user
        self.server = server

    def check(self) -> bool | None:
        if self.server.id == 740584420645535775:
            path = "/partnerships/orleans/{}.txt".format(self.user.id)
            check = os.path.exists(path)
            return True if check else None

        elif self.server.id == 925790259160166460:
            path = "/partnerships/hazeads/{}.txt".format(self.user.id)
            check = os.path.exists(path)
            return True if check else None

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
            msg = "Partnership denied AND reason sent"
        except Forbidden:
            msg = "Partnership denied"
        await ctx.followup.send(msg)


class Break:
    def __init__(self, member: Optional[Member] = None) -> None:
        self.member = member

    @staticmethod
    def check_breaks() -> list | None:
        data = db.execute("SELECT * FROM breakData WHERE accepted = ?", (1,)).fetchall()
        db.commit()
        return data if data else None

    async def remove(self):
        db.execute("DELETE FROM breakData WHERE user_id = ?", (self.member.id,))
        db.commit()

    async def cancel(self, server: int):
        approved = self.check(server)
        if approved[4] == 0:
            db.execute(
                "DELETE FROM breakData WHERE user_id = ? AND approved = ?",
                (
                    self.member.id,
                    0,
                ),
            )
            db.commit()

    async def add_request(
        self,
        server: int,
        duration: str,
        reason: str,
        accepted: int,
        start: int,
        ends: int,
    ):
        data = db.execute(
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

        if data.rowcount == 0:
            db.execute(
                "UPDATE breakData SET duration = ?, reason = ?, accepted = ?, start = ?, ends = ? WHERE user_id = ? AND guild_id = ?",
                (
                    duration,
                    reason,
                    accepted,
                    start,
                    ends,
                    self.member.id,
                    server,
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
        return data if data else None

    async def approve(self, server: int, start: int, ends: int):
        db.execute(
            "UPDATE breakData SET accepted = ?, start = ?, ends = ? WHERE user_id = ? AND guild_id = ?",
            (
                1,
                start,
                ends,
                self.member.id,
                server,
            ),
        )
        db.commit()

    async def deny(self, server: int):
        db.execute(
            "DELETE FROM breakData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                server,
            ),
        )
        db.commit()

    async def end(self, server: int):
        db.execute(
            "DELETE FROM breakData WHERE user_id = ? AND guild_id = ?",
            (
                self.member.id,
                server,
            ),
        )
        db.commit()


class Resign:
    def __init__(self, member: Member):
        self.member = member

    def apply(self, leaving: bool = None):
        leave = 1 if (leaving is True) else 0

        db.execute(
            "INSERT OR IGNORE INTO resignData (user_id, accepted, leaving) VALUES (?, ?, ?)",
            (
                self.member.id,
                0,
                leave,
            ),
        )
        db.commit()

    def check(self, leaving: Optional[int]):
        data = db.execute(
            "SELECT * FROM resignData WHERE user_id = ? AND leaving = ?",
            (
                self.member.id,
                leaving,
            ),
        ).fetchone()
        db.commit()

        return data if data else None

    async def approve(self):
        db.execute(
            "UPDATE resignData SET accepted = ? WHERE user_id = ?",
            (
                1,
                self.member.id,
            ),
        )
        db.commit()

    async def deny(self):
        db.execute("DELETE FROM resignData WHERE user_id = ?", (self.member.id,))
        db.commit()

    async def resigned(self, channel: TextChannel):
        check_accepted = db.execute(
            "SELECT accepted FROM resignData WHERE user_id = ? AND leaving = ?",
            (
                self.member.id,
                1,
            ),
        ).fetchone()

        if check_accepted is None:  # if they just left without requesting for resigning
            no_resign = Embed(
                title=f"{self.member} ({self.member.id}) left the server",
                color=Color.red(),
            )
            await channel.send(embed=no_resign)

        elif (
            int(check_accepted[0]) == 0
        ):  # if they left without an accepted resignation
            not_accepted = Embed(
                title=f"{self.member} ({self.member.id}) left the server without an approved resignation",
                color=Color.red(),
            )
            await channel.send(embed=not_accepted)

        elif int(check_accepted[0]) == 1:  # if their resignation has been accepted
            db.execute("DELETE FROM resignData WHERE user_id = ?", (self.member.id,))
            db.commit()
            accepted = Embed(
                title=f"{self.member} ({self.member.id}) has resigned.",
                color=Color.green(),
            )
            await channel.send(embed=accepted)


class Plans:
    def __init__(self, server: int):
        self.server = server

    def add(self, user: Member, until: int, plan: str, claimee: User, plan_id: int):
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

        return data if data else None

    def check(self) -> list | None:
        data = db.execute(
            "SELECT * FROM planData WHERE server_id = ?", (self.server,)
        ).fetchall()
        db.commit()
        return data if data else None

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


class YouTube:
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def get_latest_vid(self):
        data = db.execute(
            "SELECT latest_video FROM youtube WHERE channel_id = ?", (self.channel,)
        ).fetchone()
        db.commit()
        return str(data[0]) if data else None

    def update_video(self, new_video: str):
        db.execute(
            "UPDATE youtube SET latest_video = ? WHERE channel_id = ?",
            (
                new_video,
                self.channel,
            ),
        )
        db.commit()

    def get_channel(self):
        data = db.execute(
            "SELECT channel_name FROM youtube WHERE channel_id = ?", (self.channel,)
        ).fetchone()[0]
        db.commit()
        return str(data)

class Verification:
    def __init__(self) -> None:
        pass

    async def add_request(self, member:Member, message:Message):
        data = db.execute("INSERT OR IGNORE INTO verificationLog (user, message_id) VALUES (?, ?)", (member.id, message.id,))
        db.execute()

        if data.rowcount == 0:
            return
    
    def check(self, member:Member):
        data=db.execute("SELECT * FROM verificationLog WHERE user = ?", (member.id,)).fetchone()
        db.execute()

        if int(data[0]) == member.id:
            return True
        return

