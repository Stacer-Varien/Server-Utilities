import asyncio
import os
from datetime import datetime, timedelta
import re
from sqlite3 import Cursor
from typing import Literal, Optional
from random import randint

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
from config import db


class Adwarn:
    def __init__(self, moderator: Optional[Member] = None) -> None:
        self.moderator = moderator

    @staticmethod
    def check_time(member: Member) -> int | None:
        data = db.execute(
            "SELECT time FROM warnData_v2 WHERE user_id = ?", (member.id,)
        ).fetchone()
        db.commit()
        return int(data[0]) if data else None

    @staticmethod
    def check_id(member: Member, moderator: Member):
        data = db.execute(
            "SELECT warn_id FROM warnData WHERE user_id = ? AND moderator_id = ?",
            (
                member.id,
                moderator.id,
            ),
        ).fetchone()
        db.commit()
        return data

    @staticmethod
    def make_id() -> int:
        return randint(1, 999999)

    @staticmethod
    def make_new_time() -> datetime:
        current_time = datetime.now()
        return current_time + timedelta(minutes=30)

    @staticmethod
    def points(member: Member) -> int | None:
        data = db.execute(
            "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member.id,)
        ).fetchone()
        db.commit()
        return int(data[0]) if data else None

    async def punishment_rules(self, member: Member) -> str | None:
        points = self.points(member)
        embed = Embed(color=Color.red())

        if points <= 5:
            return "No punishment applied"

        if points == 6:
            duration = datetime.now() + timedelta(hours=1)
            await member.edit(timed_out_until=duration)
            result = "Put on timeout until <t:{}:f>".format(round(duration.timestamp()))
            embed.description = "You have been **{}** in HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            return result

        if points == 7:
            duration = datetime.now() + timedelta(hours=12)
            await member.edit(timed_out_until=duration)
            result = "Put on timeout until <t:{}:f>".format(round(duration.timestamp()))
            embed.description = "You have been **{}** in HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            return result

        if points == 8:
            duration = datetime.now() + timedelta(days=1)
            await member.edit(timed_out_until=duration)
            result = "Put on timeout until <t:{}:f>".format(round(duration.timestamp()))
            embed.description = "You have been **{}** in HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            return result

        if points == 9:
            await member.kick(reason="Reached 9 points")
            result = "Kick"
            embed.description = "You have been **{}** from HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            return result

        if points == 10:
            await member.ban(reason="Reached 10 points")
            result = "Permanent Ban"
            embed.description = "You have been **{}** from HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            return result

    async def add(self, member: Member, reason: str) -> Literal[False] | None:
        current_time = round(datetime.now().timestamp())
        time = self.check_time(member)

        if (current_time >= time) or (time == None):
            warn_id = self.make_id()
            adwarn_channel = await member.guild.fetch_channel(925790260695281703)
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id) VALUES (?,?,?,?)",
                (
                    member.id,
                    self.moderator.id,
                    reason,
                    warn_id,
                ),
            )
            db.execute(
                "INSERT OR IGNORE INTO warnData_2 (user_id, warn_point, time) VALUES (?,?,?)",
                (
                    member.id,
                    1,
                    self.make_new_time(),
                ),
            )
            db.commit()

            if (
                db.execute(
                    "UPDATE warnData_v2 SET warn_point = warn_point + 1, time = ? WHERE user_id = ?",
                    (self.make_new_time(), member.id),
                ).rowcount
                == 0
            ):
                db.commit()
            embed = Embed()
            embed.title = "You have been adwarned"
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.add_field(name="Warn ID", value=warn_id, inline=True)
            embed.add_field(name="Warn Points", value=self.points(member), inline=True)
            punishment = await self.punishment_rules(member)
            embed.add_field(name="Punishment", value=punishment, inline=True)
            embed.set_footer(
                text="If you feel this warn was a mistake, please use `/appeal WARN_ID` or open a ticket"
            )
            await adwarn_channel.send(member.mention, embed=embed)
            return

        return False

    async def remove(self, member: Member, moderator: Member) -> Literal[False] | None:
        data = self.check_id(member, moderator)
        if not data:
            return

        db.execute(
            "DELETE FROM warnData WHERE user_id = ? AND moderator_id = ? AND warn_id = ?",
            (
                member.id,
                moderator.id,
                int(data[1]),
            ),
        )
        db.execute(
            "UPDATE warnData_v2 SET warn_point = warn_point - 1 WHERE user_id = ?",
            (member.id,),
        )
        db.commit()

        if self.points(member) == 0:
            db.execute("DELETE FROM warnData_v2 WHERE user_id = ?", (member.id,))
            db.commit()


class AutoMod:
    def __init__(self, bot: Bot, message: Message) -> None:
        self.bot = bot
        self.message = message

    with open("assets/not_allowed.json", "r") as f:
        jsondata = f.readlines()

    async def adwarn(self):
        global invite_url
        not_allowed_channels = [int(i) for i in self.jsondata["no_invites_allowed"]]
        advertising_cat = await self.message.guild.fetch_channel(925790260695281702)
        if not self.message.author:
            if "https://discord.gg/" in self.message.content:
                if self.message.channel.id in not_allowed_channels:
                    await self.message.delete()
                    if self.message.guild.id == 925790259160166460:
                        await Adwarn(self.bot.user).add(
                            self.message.author,
                            "Incorrectly advertising in non-Discord advertising channels",
                        )
                        return

            if self.message.id in [
                i.id
                for i in advertising_cat.channels
                if not (i.id == 951385958924828713)
            ]:
                if len(self.message.content) <= 40:
                    await self.message.delete()
                    await Adwarn(self.bot.user).add(
                        self.message.author,
                        "Discord server ad contains less than 40 characters (too short)",
                    )
                    return

    async def check_expired(self):
        invite_pattern = re.compile(
            r"(discord\.gg/|discord\.com/invite/)([a-zA-Z0-9]+)"
        )
        match = invite_pattern.search(self.message.content)
        if match:
            invite_url = f"https://discord.gg/{match.group(2)}"

        try:
            invite = await self.bot.fetch_invite(invite_url)
        except:
            await message.delete()
            await Adwarn(self.bot.user).add(
                self.message.author,
                "Discord server invite is expired",
            )
            return

    async def remove_non_attachments(self):
        if self.message.guild.id == 925790259160166460:
            attachments = bool(self.message.attachments)
            content = bool(self.message.content)
            stickers = bool(self.message.stickers)

            if (content and not attachments) or (not content and stickers):
                await self.message.delete()
                return
            if (
                (content and attachments)
                or (attachments and not content)
                or (stickers and attachments)
                or (stickers and attachments and content)
            ):
                return


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
            (plan_id, self.server),
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
            (buyer.id, plan_id, self.server),
        )
        db.commit()


class YouTube:
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def get_latest_vid(self):
        return (
            db.execute(
                "SELECT latest_video FROM youtube WHERE channel_id = ?", (self.channel,)
            ).fetchone()[0]
            or None
        )

    def update_video(self, new_video: str):
        db.execute(
            "UPDATE youtube SET latest_video = ? WHERE channel_id = ?",
            (new_video, self.channel),
        )
        db.commit()

    def get_channel(self):
        return (
            db.execute(
                "SELECT channel_name FROM youtube WHERE channel_id = ?", (self.channel,)
            ).fetchone()[0]
            or None
        )


class Verification:
    def __init__(self) -> None:
        pass

    async def add_request(self, member: Member, message: Message):
        db.execute(
            "INSERT OR IGNORE INTO verificationLog (user, message_id) VALUES (?, ?)",
            (member.id, message.id),
        )
        db.commit()

    def check_user(self, message: Message, member: Optional[Member] = None):
        data = db.execute(
            "SELECT user FROM verificationLog WHERE message_id = ?", (message.id,)
        ).fetchone()
        return message.guild.get_member(data[0]) if data else None

    def check(self, message: Optional[Message] = None):
        member = self.check_user(message)
        data = db.execute(
            "SELECT * FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        ).fetchone()
        db.commit()

        verify_role = member.guild.get_role(974760640742825984)

        if data and (
            (int(data[0]) == member.id and int(data[1]) == message.id)
            or int(data[0]) == member.id
        ):
            return True

        return verify_role in member.roles

    async def approve(self, message: Message):
        member = self.check_user(message)
        db.execute(
            "DELETE FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        )
        db.commit()

        verify_role = member.guild.get_role(974760640742825984)
        member_role = member.guild.get_role(974760599487647815)
        untrusted = member.guild.get_role(974760534102650950)

        await member.add_roles(verify_role, reason="Successfully verified")

        if untrusted in member.roles:
            await member.remove_roles(untrusted, "Successful forced verification")
            await member.add_roles(member_role)

    async def deny(self, message: Message):
        member = self.check_user(message)
        db.execute(
            "DELETE FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        )
        db.commit()

    async def force(self, member: Member):
        untrusted = member.guild.get_role(974760534102650950)
        for role in member.roles:
            await member.remove_roles(role, "Removed due to forced verification")
            await asyncio.sleep(1)
        await member.add_roles(untrusted, "Force verification")
