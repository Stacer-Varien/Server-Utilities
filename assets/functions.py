import asyncio
from json import loads
import os
from datetime import datetime, timedelta
import re
from typing import Literal, Optional
from random import randint
from discord.ext.commands import Context

from discord import (
    Color,
    Embed,
    Guild,
    Interaction,
    Invite,
    Member,
    Message,
    PartialInviteGuild,
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
    def check_id(member: Member, warn_id: int):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ? AND warn_id = ?",
            (
                member.id,
                warn_id,
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
            try:
                await member.send(embed=embed)
            except:
                pass
            return result

        if points == 7:
            duration = datetime.now() + timedelta(hours=12)
            await member.edit(timed_out_until=duration)
            result = "Put on timeout until <t:{}:f>".format(round(duration.timestamp()))
            embed.description = "You have been **{}** in HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            try:
                await member.send(embed=embed)
            except:
                pass
            return result

        if points == 8:
            duration = datetime.now() + timedelta(days=1)
            await member.edit(timed_out_until=duration)
            result = "Put on timeout until <t:{}:f>".format(round(duration.timestamp()))
            embed.description = "You have been **{}** in HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            try:
                await member.send(embed=embed)
            except:
                pass
            return result

        if points == 9:
            await member.kick(reason="Reached 9 points")
            result = "Kick"
            embed.description = "You have been **{}** from HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            try:
                await member.send(embed=embed)
            except:
                pass
            return result

        if points == 10:
            await member.ban(reason="Reached 10 points")
            result = "Permanent Ban"
            embed.description = "You have been **{}** from HAZE Advertising for reaching {} points".format(
                result.lower(), str(self.points(member))
            )
            try:
                await member.send(embed=embed)
            except:
                pass
            return result

    async def add(self, member: Member, channel: TextChannel, reason: str):
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
        embed = Embed(color=Color.red())
        embed.title = "You have been adwarned"
        embed.add_field(
            name="Channel where the incident happened",
            value=channel.mention,
            inline=True,
        )
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Warn ID", value=warn_id, inline=True)
        embed.add_field(name="Warn Points", value=self.points(member), inline=True)
        punishment = await self.punishment_rules(member)
        embed.add_field(name="Punishment", value=punishment, inline=True)
        embed.set_footer(
            text="If you feel this warn was a mistake, please use `/appeal WARN_ID` or open a ticket"
        )
        embed.set_thumbnail(url=member.display_avatar)
        await adwarn_channel.send(member.mention, embed=embed)

        def is_member(m: Message):
            return m.author == member

        for i in member.guild.text_channels:
            try:
                await i.purge(limit=3, check=is_member)
            except:
                continue
        return

    async def remove(self, member: Member, warn_id: int):
        data = self.check_id(member, warn_id)
        if not data:
            return

        db.execute(
            "DELETE FROM warnData WHERE user_id = ? AND warn_id = ?",
            (
                member.id,
                warn_id,
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
    def __init__(self, bot: Bot, message: Message):
        self.bot = bot
        self.message = message
        self.advertising_cat_id = 925790260695281702
        self.blacklist_channel_id = 951385958924828713

    with open("assets/not_allowed.json", "r") as f:
        jsondata: dict = loads("".join(f.readlines()))

    async def process_automod(self):
        if not self.message.author.bot:
            content = self.message.content
            channel_id = self.message.channel.id
            not_allowed_channels = [int(i) for i in self.jsondata["no_invites_allowed"]]

            if self.message.guild.id == 925790259160166460:
                advertising_cat = await self.message.guild.fetch_channel(
                    self.advertising_cat_id
                )
                if (
                    channel_id == advertising_cat.id
                    and self.message.id
                    in [
                        i.id
                        for i in advertising_cat.channels
                        if i.id != self.blacklist_channel_id
                    ]
                    and len(content) <= 40
                ):
                    await self.handle_short_ad()
                    return

                if self.message.id in [i.id for i in advertising_cat.channels] and (
                    match := re.search(
                        r"(discord\.gg/|discord\.com/invite/)([a-zA-Z0-9]+)", content
                    )
                ):
                    invite_url = (
                        f"https://discord.gg/{match.group(2)}"
                        or f"https://discord.com/invite/{match.group(2)}"
                    )
                    await self.check_invite(invite_url)
                    await self.check_invite(invite_url, check_blacklist=True)
                    return

            if (
                "https://discord.gg/" or "https://discord.com/invite/"
            ) in content and channel_id in not_allowed_channels:
                allowed_channels = [
                    1048509171496144926,
                    1055055791469645845,
                    1045341985654964334,
                    1040380792406298645,
                    1003576509858058290,
                    1037336353593114754,
                    1040883460547559474,
                    770263931334950912,
                    1045342152726683748,
                    925790259877412875,
                    925790259877412877,
                    925790259877412876,
                    925790259877412878,
                    925790259877412879,
                    947936542561804348,
                    949656142001348628,
                    954696784263905290,
                    1003970769036001330,
                    980732864884781106,
                    1055055791469645845,
                    974028573893595149,
                    974753944792358923,
                    974760508240576553,
                    991644325492568084,
                    1003576509858058290,
                    1055046171929878541,
                    1058385832827949066,
                    1059903781552267294,
                    1086761697420783778,
                    1153987641264586836,
                    1181585427837227058,
                    1059931943917076570,
                ]
                if self.message.channel.id not in allowed_channels:
                    await self.handle_advertising()
                    return

        if self.message.channel.id == 1041309643449827360:
            attachments = bool(self.message.attachments)
            content = bool(self.message.content)
            stickers = bool(self.message.stickers)

            if (content and not attachments) or (not content and stickers):
                await self.message.delete()

    async def handle_advertising(self):
        await self.message.delete()
        if self.message.guild.id == 925790259160166460:
            await Adwarn(self.bot.user).add(
                self.message.author,
                self.message.channel.mention,
                "**Incorrectly advertising** in non-Discord advertising channels",
            )

    async def handle_short_ad(self):
        await self.message.delete()
        await Adwarn(self.bot.user).add(
            self.message.author,
            self.message.channel.mention,
            "Discord server ad contains less than **40 characters** (too short)",
        )

    async def check_invite(self, invite_url: str, check_blacklist=False):
        try:
            invite = await self.bot.fetch_invite(invite_url)

            if check_blacklist and invite.id in self.get_blacklisted_servers:
                await self.handle_blacklisted_server()
                return

            await self.check_invite_expiration(invite)

        except:
            await self.message.delete()
            await Adwarn(self.bot.user).add(
                self.message.author,
                self.message.channel.mention,
                "Discord server invite is **invalid**",
            )

    async def check_invite_expiration(self, invite: Invite | PartialInviteGuild):
        after_7_days = invite.created_at.now() + timedelta(days=7)
        invite_expiration = invite.expires_at

        if round(invite_expiration.timestamp()) < round(after_7_days.timestamp()):
            await self.message.delete()
            await Adwarn(self.bot.user).add(
                self.message.author,
                self.message.channel.mention,
                "Discord server invite should not be valid for less than **7 days**",
            )

    async def handle_blacklisted_server(self):
        await self.message.delete()
        await Adwarn(self.bot.user).add(
            self.message.author,
            self.message.channel.mention,
            "Advertising a **blacklisted server**",
        )

    @property
    def get_blacklisted_servers(self):
        return [
            record[0]
            for record in db.execute(
                "SELECT server_id FROM blacklistedServersData"
            ).fetchall()
        ]


class Partner:
    def __init__(self, server: Guild):
        self.server = server

    def check(self, member: Member) -> bool | None:
        if self.server.id == 740584420645535775:
            path = "/partnerships/orleans/{}.txt".format(member.id)
            check = os.path.exists(path)
            return True if check else None

        elif self.server.id == 925790259160166460:
            path = "/partnerships/hazeads/{}.txt".format(member.id)
            check = os.path.exists(path)
            return True if check else None

    async def approve(self, ctx: Interaction, member: Member):
        if self.server.id == 740584420645535775:
            with open("partnerships/orleans/{}.txt".format(member.id), "r") as f:
                content = "".join(f.readlines())
            os.remove("partnerships/orleans/{}.txt".format(member.id))
            partner_role = self.server.get_role(1051047558224543844)
            if partner_role in member.roles:
                pass
            else:
                await member.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(1040380792406298645)
            await partner_channnel.send(content=content)
        elif self.server.id == 925790259160166460:
            with open("partnerships/hazeads/{}.txt".format(member.id), "r") as f:
                content = "".join(f.readlines())
            os.remove("partnerships/hazeads/{}.txt".format(member.id))
            partner_role = self.server.get_role(950354444669841428)
            if partner_role in member.roles:
                pass
            else:
                await member.add_roles(partner_role, reason="New Partner")
            partner_channnel = await self.server.fetch_channel(1040380792406298645)
            await partner_channnel.send(content=content)
        await ctx.followup.send("Partnership approved")

    async def deny(self, ctx: Interaction, member: Member, reason: str):
        if self.server.id == 740584420645535775:
            os.remove("partnerships/orleans/{}.txt".format(member.id))
        elif self.server.id == 925790259160166460:
            os.remove("partnerships/hazeads/{}.txt".format(member.id))

        try:
            await member.send(f"Your partnership request was denied because:\n{reason}")
            msg = "Partnership denied AND reason sent"
        except Forbidden:
            msg = "Partnership denied"
        await ctx.followup.send(msg)


class Plans:
    def __init__(self):
        pass

    def add(self, user: Member, until: int, plan: str, claimee: User, plan_id: int):
        db.execute(
            "INSERT OR IGNORE INTO planData (user_id, started, until, plans, set_by, plan_id) VALUES (?,?,?,?,?,?)",
            (
                user.id,
                round(datetime.now().timestamp()),
                until,
                plan,
                claimee.id,
                plan_id,
            ),
        )
        db.commit()

    def get(self, buyer: Member, plan_id: int):
        data = db.execute(
            "SELECT * FROM planData WHERE plan_id = ? AND user_id = ?",
            (
                plan_id,
                buyer.id,
            ),
        ).fetchone()

        return data if data else None

    def check(self) -> list | None:
        data = db.execute("SELECT * FROM planData").fetchall()
        db.commit()
        return data if data else None

    def remove(self, buyer: User, plan_id: int):
        db.execute(
            "DELETE FROM planData WHERE user_id = ? AND plan_id= ?",
            (
                buyer.id,
                plan_id,
            ),
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


class Blacklist:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def get_blacklisted_servers(self):
        data = db.execute("SELECT server_id FROM blacklistedServersData").fetchall()
        return data

    @staticmethod
    async def add(server_id: str, reason: str):
        db.execute(
            "INSERT OR IGNORE INTO blacklistedServersData (server_id, reason) VALUES (?, ?)",
            (server_id, reason),
        )
        db.commit()

    @staticmethod
    async def remove(server_id: int):
        db.execute(
            "DELETE FROM blacklistedServersData WHERE server_id = ?", (server_id,)
        )
        db.commit()

    async def _handle_blacklist_action(
        self,
        ctx: Context,
        invite_url: str,
        reason: str,
        action_message: str,
        unblacklist=False,
    ):
        try:
            invite = await self.bot.fetch_invite(invite_url)
            channel = await ctx.guild.fetch_channel(1201991756950806538)
            embed = Embed(color=Color.red())
            embed.title = action_message
            embed.add_field(name="Name", value=invite.guild.name, inline=True)
            embed.add_field(name="ID", value=invite.guild.id, inline=True)
            embed.set_thumbnail(url=invite.guild.icon)
            description_prefix = "# Reason of"
            action_description = "Un" if unblacklist else ""
            embed.description = (
                f"{description_prefix} {action_description}blacklist:\n\n{reason}"
            )
            if unblacklist:
                await self.remove(invite.guild.id)
                await channel.send(embed=embed)
            else:
                await self.add(invite.guild.id, reason)
                await channel.send(embed=embed)
        except:
            await self._handle_invalid_invite(ctx)

    async def _handle_invalid_invite(self, ctx: Context):
        invalid_invite_message = "Invalid or expired invite"
        await ctx.reply(invalid_invite_message, delete_after=5)
        await ctx.message.delete()


class Currency:
    def __init__(self, user: User):
        self.user = user

    @property
    def get_balance(self) -> int:
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()

        return int(data[0]) if data else 0

    async def add_credits(self, amount: int):
        current_time=datetime.now()
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                amount,
                (current_time - timedelta(days=1)),
            ),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET amount = amount + ? WHERE user_id = ?",
                (
                    amount,
                    self.user.id,
                ),
            )

            db.commit()

    async def remove_credits(self, amount: int):
        db.execute(
            "UPDATE bankData SET amount = amount - ? WHERE user_id = ?",
            (
                amount,
                self.user.id,
            ),
        )

        db.commit()

    async def give_daily(self):
        next_claim = round((datetime.now() + timedelta(days=1)).timestamp())

        credits = 200 if (datetime.today().weekday() >= 5) else 100

        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (
                self.user.id,
                credits,
                next_claim,
            ),
        )
        db.commit()
        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET claimed_date = ?, amount = amount + ? WHERE user_id = ?",
                (
                    next_claim,
                    credits,
                    self.user.id,
                ),
            )
            db.commit()

    @property
    def check_daily(self) -> int | Literal[True]:
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()
        if (data == None) or (int(data[0]) < round(datetime.now().timestamp())):
            return True
        return int(data[0])
