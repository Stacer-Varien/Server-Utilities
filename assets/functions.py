import asyncio
from json import loads
import os
from datetime import datetime, timedelta
import re
from typing import List, Literal, Optional, Union
from random import randint
from discord.ext.commands import Context
from ad_chan_rules import not_allowed, allowed_ads

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
            (member.id, warn_id),
        ).fetchone()
        db.commit()
        return data

    @staticmethod
    def make_id() -> int:
        return randint(1, 999999)

    @staticmethod
    def make_new_time() -> datetime:
        return datetime.now() + timedelta(minutes=30)

    @staticmethod
    def points(member: Member) -> int | None:
        data = db.execute(
            "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member.id,)
        ).fetchone()
        db.commit()
        return int(data[0]) if data else None

    async def punishment_rules(self, member: Member) -> str | None:
        points = self.points(member)
        if points is None:
            return None

        punishments = [
            (6, timedelta(hours=1), "timeout"),
            (7, timedelta(hours=12), "timeout"),
            (8, timedelta(days=1), "timeout"),
            (9, None, "kick"),
            (10, None, "ban"),
        ]

        embed = Embed(color=Color.red())

        for point, duration, action in punishments:
            if points == point:
                if action == "timeout":
                    duration = datetime.now() + duration
                    await member.edit(timed_out_until=duration)
                    result = f"Put on timeout until <t:{round(duration.timestamp())}:f>"
                elif action == "kick":
                    await member.kick(reason="Reached 9 points")
                    result = "Kick"
                elif action == "ban":
                    await member.ban(reason="Reached 10 points")
                    result = "Permanent Ban"

                embed.description = f"You have been **{result.lower()}** in HAZE Advertising for reaching {points} points"
                try:
                    await member.send(embed=embed)
                except Exception as e:
                    print(f"Failed to send embed to member: {e}")
                return result

        return "No punishment applied"

    async def add(self, member: Member, channel: TextChannel, reason: str):
        warn_id = self.make_id()
        adwarn_channel = await member.guild.fetch_channel(1239564619131912222)
        current_time = self.make_new_time()

        db.execute(
            "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id) VALUES (?, ?, ?, ?)",
            (member.id, self.moderator.id, reason, warn_id),
        )
        db.execute(
            "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?, ?, ?)",
            (member.id, 1, current_time),
        )
        db.execute(
            "UPDATE warnData_v2 SET warn_point = warn_point + 1, time = ? WHERE user_id = ?",
            (current_time, member.id),
        )
        db.commit()

        embed = Embed(color=Color.red(), title="You have been adwarned")
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
        embed.set_thumbnail(url=member.display_avatar.url)
        await adwarn_channel.send(member.mention, embed=embed)

        def is_member(m: Message):
            return m.author == member

        for channel in member.guild.text_channels:
            try:
                await channel.purge(limit=3, check=is_member)
            except Exception as e:
                print(f"Failed to purge messages in {channel.name}: {e}")

    async def remove(self, member: Member, warn_id: int):
        if not self.check_id(member, warn_id):
            return

        db.execute(
            "DELETE FROM warnData WHERE user_id = ? AND warn_id = ?",
            (member.id, warn_id),
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

    async def process_automod(self):
        if not self.message.author.bot:
            content = self.message.content
            channel_id = self.message.channel.id

            if self.message.guild.id == 925790259160166460:
                if (
                    channel_id in allowed_ads
                    and self.message.id in allowed_ads
                    and channel_id not in not_allowed
                    and len(content) <= 40
                ):
                    await self.handle_short_ad()
                    return

                if self.message.id in allowed_ads and (
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
                any(
                    url in content
                    for url in ["https://discord.gg/", "https://discord.com/invite/"]
                )
                and channel_id in not_allowed
            ):
                await self.handle_advertising()
                return

        if self.message.channel.id == 1041309643449827360:
            attachments = bool(self.message.attachments)
            content = bool(self.message.content)
            stickers = bool(self.message.stickers)

            if (content and not attachments) or (not content and stickers):
                await self.message.delete()

    async def handle_advertising(self):
        message = self.message
        await message.delete()
        if message.guild.id == 925790259160166460:
            await Adwarn(self.bot.user).add(
                message.author,
                message.channel.mention,
                "**Incorrectly advertising** in non-Discord advertising channels",
            )

    async def handle_short_ad(self):
        message=self.message
        await message.delete()
        await Adwarn(self.bot.user).add(
            message.author,
            message.channel.mention,
            "Discord server ad contains less than **40 characters** (too short)",
        )

    async def check_invite(self, invite_url: str, check_blacklist=False):
        try:
            invite = await self.bot.fetch_invite(invite_url)

            if check_blacklist and invite.id in self.get_blacklisted_servers:
                await self.handle_blacklisted_server()
                return

            await self.check_invite_expiration(invite)

        except Exception:
            message = self.message
            await message.delete()
            await Adwarn(self.bot.user).add(
                message.author,
                message.channel.mention,
                "Discord server invite is **invalid**",
            )

    async def check_invite_expiration(self, invite: Invite | PartialInviteGuild):
        after_7_days = invite.created_at + timedelta(days=7)
        invite_expiration = invite.expires_at

        if invite_expiration and invite_expiration < after_7_days:
            message = self.message
            await self.message.delete()
            await Adwarn(self.bot.user).add(
                message.author,
                message.channel.mention,
                "Discord server invite should not be valid for less than **7 days**",
            )

    async def handle_blacklisted_server(self):
        message = self.message
        await message.delete()
        await Adwarn(self.bot.user).add(
            message.author,
            message.channel.mention,
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
    PARTNERSHIP_DATA = {
        740584420645535775: {
            "path": "/partnerships/orleans/{}.txt",
            "role_id": 1051047558224543844,
            "channel_id": 1040380792406298645,
        },
        925790259160166460: {
            "path": "/partnerships/oad/{}.txt",
            "role_id": 950354444669841428,
            "channel_id": 1040380792406298645,
        },
    }

    def __init__(self, server: Guild):
        self.server = server
        self.config = self.PARTNERSHIP_DATA.get(server.id)

    def check(self, member: Member) -> bool | None:
        if self.config:
            path = self.config["path"].format(member.id)
            return os.path.exists(path) or None

    async def approve(self, ctx: Interaction, member: Member):
        if self.config:
            path = self.config["path"].format(member.id)
            with open(path, "r") as f:
                content = f.read()
            os.remove(path)

            partner_role = self.server.get_role(self.config["role_id"])
            if partner_role not in member.roles:
                await member.add_roles(partner_role, reason="New Partner")

            partner_channel = await self.server.fetch_channel(self.config["channel_id"])
            await partner_channel.send(content=content)
            await ctx.followup.send("Partnership approved")

    async def deny(self, ctx: Interaction, member: Member, reason: str):
        if self.config:
            path = self.config["path"].format(member.id)
            os.remove(path)

        try:
            await member.send(f"Your partnership request was denied because:\n{reason}")
            msg = "Partnership denied AND reason sent"
        except Forbidden:
            msg = "Partnership denied"

        await ctx.followup.send(msg)


class Plans:
    @staticmethod
    def add(user: Member, until: int, plan: str, claimee: User, plan_id: int):
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

    @staticmethod
    def get(buyer: Member, plan_id: int) -> Optional[dict]:
        data = db.execute(
            "SELECT * FROM planData WHERE plan_id = ? AND user_id = ?",
            (plan_id, buyer.id),
        ).fetchone()
        return data

    @staticmethod
    def check() -> Optional[List[dict]]:
        data = db.execute("SELECT * FROM planData").fetchall()
        return data if data else None

    @staticmethod
    def remove(buyer: User, plan_id: int):
        db.execute(
            "DELETE FROM planData WHERE user_id = ? AND plan_id = ?",
            (buyer.id, plan_id),
        )
        db.commit()


class YouTube:
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def get_latest_vid(self):
        result = db.execute(
            "SELECT latest_video FROM youtube WHERE channel_id = ?", (self.channel,)
        ).fetchone()
        return result[0] if result else None

    def update_video(self, new_video: str):
        db.execute(
            "UPDATE youtube SET latest_video = ? WHERE channel_id = ?",
            (new_video, self.channel),
        )
        db.commit()

    def get_channel(self):
        result = db.execute(
            "SELECT channel_name FROM youtube WHERE channel_id = ?", (self.channel,)
        ).fetchone()
        return result[0] if result else None


class Verification:
    VERIFY_ROLE_ID = 974760640742825984
    MEMBER_ROLE_ID = 974760599487647815
    UNTRUSTED_ROLE_ID = 974760534102650950

    def __init__(self) -> None:
        pass

    async def add_request(self, member: Member, message: Message):
        db.execute(
            "INSERT OR IGNORE INTO verificationLog (user, message_id) VALUES (?, ?)",
            (member.id, message.id),
        )
        db.commit()

    def check_user(self, message: Message) -> Optional[Member]:
        data = db.execute(
            "SELECT user FROM verificationLog WHERE message_id = ?", (message.id,)
        ).fetchone()
        return message.guild.get_member(data[0]) if data else None

    def check(self, message: Message) -> bool:
        member = self.check_user(message)
        if not member:
            return False

        data = db.execute(
            "SELECT * FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        ).fetchone()
        db.commit()

        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)

        if data:
            return True

        return verify_role in member.roles

    async def approve(self, message: Message):
        member = self.check_user(message)
        if not member:
            return

        db.execute(
            "DELETE FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        )
        db.commit()

        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)
        member_role = member.guild.get_role(self.MEMBER_ROLE_ID)
        untrusted = member.guild.get_role(self.UNTRUSTED_ROLE_ID)

        await member.add_roles(verify_role, reason="Successfully verified")

        if untrusted in member.roles:
            await member.remove_roles(
                untrusted, reason="Successful forced verification"
            )
            await member.add_roles(member_role, reason="Add member role")

    async def deny(self, message: Message):
        member = self.check_user(message)
        if not member:
            return

        db.execute(
            "DELETE FROM verificationLog WHERE user = ? AND message_id = ?",
            (member.id, message.id),
        )
        db.commit()

    async def force(self, member: Member):
        untrusted = member.guild.get_role(self.UNTRUSTED_ROLE_ID)
        for role in member.roles:
            if role.id != untrusted.id:
                await member.remove_roles(
                    role, reason="Removed due to forced verification"
                )
                await asyncio.sleep(1)
        await member.add_roles(untrusted, reason="Force verification")


class Blacklist:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def get_blacklisted_servers(self):
        data = db.execute("SELECT server_id FROM blacklistedServersData").fetchall()
        return [record[0] for record in data]

    async def add(self, server_id: str, reason: str):
        db.execute(
            "INSERT OR IGNORE INTO blacklistedServersData (server_id, reason) VALUES (?, ?)",
            (server_id, reason),
        )
        db.commit()

    async def remove(self, server_id: str):
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
        unblacklist: bool = False,
    ):
        try:
            invite = await self.bot.fetch_invite(invite_url)
            channel = await ctx.guild.fetch_channel(1201991756950806538)
            embed = Embed(color=Color.red())
            embed.title = action_message
            embed.add_field(name="Name", value=invite.guild.name, inline=True)
            embed.add_field(name="ID", value=invite.guild.id, inline=True)
            embed.set_thumbnail(url=invite.guild.icon)

            action_description = "Unblacklist" if unblacklist else "Blacklist"
            embed.description = f"# Reason of {action_description}:\n\n{reason}"

            if unblacklist:
                await self.remove(invite.guild.id)
            else:
                await self.add(invite.guild.id, reason)

            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error handling invite: {e}")
            await self._handle_invalid_invite(ctx)

    async def _handle_invalid_invite(self, ctx: Context):
        invalid_invite_message = "Invalid or expired invite"
        await ctx.reply(invalid_invite_message, delete_after=5)
        await ctx.message.delete()


class Currency:
    def __init__(self, user: User):
        self.user = user

    @property
    def balance(self) -> int:
        data = db.execute(
            "SELECT amount FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        return int(data[0]) if data else 0

    async def add_credits(self, amount: int):
        current_time = datetime.now() - timedelta(days=1)
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (self.user.id, amount, current_time),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET amount = amount + ? WHERE user_id = ?",
                (amount, self.user.id),
            )
            db.commit()

    async def remove_credits(self, amount: int):
        db.execute(
            "UPDATE bankData SET amount = amount - ? WHERE user_id = ?",
            (amount, self.user.id),
        )
        db.commit()

    async def give_daily(self):
        next_claim = datetime.now() + timedelta(days=1)
        next_claim_timestamp = round(next_claim.timestamp())
        credits = 200 if datetime.today().weekday() >= 5 else 100

        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount, claimed_date) VALUES (?,?,?)",
            (self.user.id, credits, next_claim_timestamp),
        )
        db.commit()

        if cur.rowcount == 0:
            db.execute(
                "UPDATE bankData SET claimed_date = ?, amount = amount + ? WHERE user_id = ?",
                (next_claim_timestamp, credits, self.user.id),
            )
            db.commit()

    @property
    def check_daily(self) -> Union[int, bool]:
        data = db.execute(
            "SELECT claimed_date FROM bankData WHERE user_id = ?", (self.user.id,)
        ).fetchone()
        db.commit()

        if data is None or int(data[0]) >= round(datetime.now().timestamp()):
            return True
        return int(data[0])
