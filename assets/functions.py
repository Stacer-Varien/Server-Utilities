import asyncio
from typing import Optional

from discord import (
    Member,
    Message,
)
from discord.ext.commands import Bot
from config import db


class AutoMod:
    def __init__(self, bot: Bot, message: Message):
        self.bot = bot
        self.message = message

    async def process_automod(self):
        if not self.message.author.bot:
            content = self.message.content
            channel_id = self.message.channel.id

            if any(
                url in content
                for url in ["https://discord.gg/", "https://discord.com/invite/"]
            ) and channel_id not in [
                925790259160166460,
                1040380792406298645,
                1101129617017950288,
                1003576509858058290,
                1086733654476197978,
            ]:
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

    async def check_invite(self, invite_url: str, check_blacklist=False):
        try:
            invite = await self.bot.fetch_invite(invite_url)

            if check_blacklist and invite.id in self.get_blacklisted_servers:
                await self.handle_blacklisted_server()
                return

        except Exception:
            return

    async def handle_blacklisted_server(self):
        message = self.message
        await message.delete()

    @property
    def get_blacklisted_servers(self):
        return [
            record[0]
            for record in db.execute(
                "SELECT server_id FROM blacklistedServersData"
            ).fetchall()
        ]


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
