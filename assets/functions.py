import re
from typing import Optional

from discord import (
    HTTPException,
    Member,
    Message,
)
from discord.ext.commands import Bot
from config import db


class AutoMod:
    INVITE_PATTERN = re.compile(
        r"(?:https?://)?(?:discord\.gg|discord\.com/invite)/[A-Za-z0-9-]+",
        re.IGNORECASE,
    )

    def __init__(self, bot: Bot, message: Message):
        self.bot = bot
        self.message = message

    async def process_automod(self) -> bool:
        if self.message.guild is None:
            return False

        content = self.message.content
        channel_id = self.message.channel.id

        invite_urls = [
            match.group(0)
            if match.group(0).lower().startswith(("http://", "https://"))
            else f"https://{match.group(0)}"
            for match in self.INVITE_PATTERN.finditer(content)
        ]
        if invite_urls:
            for invite_url in invite_urls:
                if await self.check_invite(invite_url, check_blacklist=True):
                    return True

            if channel_id not in [
                925790259160166460,
                1040380792406298645,
                1101129617017950288,
                1003576509858058290,
                1086733654476197978,
            ]:
                return await self.handle_advertising()

        if self.message.channel.id == 1041309643449827360:
            if not self.message.attachments:
                return await self.delete_message()

        return False

    async def delete_message(self) -> bool:
        try:
            await self.message.delete()
        except HTTPException:
            return False
        return True

    async def handle_advertising(self) -> bool:
        return await self.delete_message()

    async def check_invite(self, invite_url: str, check_blacklist=False) -> bool:
        try:
            invite = await self.bot.fetch_invite(invite_url)

            if (
                check_blacklist
                and invite.guild
                and invite.guild.id in self.get_blacklisted_servers
            ):
                return await self.handle_blacklisted_server()

        except HTTPException:
            pass

        return False

    async def handle_blacklisted_server(self) -> bool:
        return await self.delete_message()

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

    async def add_request(self, member: Member, message: Message) -> bool:
        cursor = db.execute(
            "INSERT OR IGNORE INTO verificationLog (user, message_id) VALUES (?, ?)",
            (member.id, message.id),
        )
        db.commit()
        return cursor.rowcount == 1

    def get_request_member(self, message: Message) -> Optional[Member]:
        if message.guild is None:
            return None
        user_id = self.get_request_user_id(message)
        return message.guild.get_member(user_id) if user_id else None

    def get_request_user_id(self, message: Message) -> Optional[int]:
        data = db.execute(
            "SELECT user FROM verificationLog WHERE message_id = ?", (message.id,)
        ).fetchone()
        return data[0] if data else None

    def check_user(self, message: Message) -> Optional[Member]:
        return self.get_request_member(message)

    def has_request_for_message(self, message: Message) -> bool:
        data = db.execute(
            "SELECT 1 FROM verificationLog WHERE message_id = ?", (message.id,)
        ).fetchone()
        return data is not None

    def has_request_for_member(self, member: Member) -> bool:
        data = db.execute(
            "SELECT 1 FROM verificationLog WHERE user = ?", (member.id,)
        ).fetchone()
        return data is not None

    def is_verified(self, member: Member) -> bool:
        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)
        return bool(verify_role and verify_role in member.roles)

    def check(self, message: Message) -> bool:
        return self.has_request_for_message(message)

    async def approve(self, message: Message, member: Optional[Member] = None):
        member = member or self.get_request_member(message)
        if not member:
            return

        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)
        member_role = member.guild.get_role(self.MEMBER_ROLE_ID)
        untrusted = member.guild.get_role(self.UNTRUSTED_ROLE_ID)

        if verify_role is None:
            raise RuntimeError("The configured verification role does not exist.")

        if member_role is None:
            raise RuntimeError("The configured member role does not exist.")

        await member.add_roles(
            verify_role,
            member_role,
            reason="Successfully verified",
        )

        if untrusted and untrusted in member.roles:
            await member.remove_roles(
                untrusted, reason="Successful forced verification"
            )

        self.remove_request(message)

    async def deny(self, message: Message):
        self.remove_request(message)

    def remove_request(self, message: Message):
        db.execute(
            "DELETE FROM verificationLog WHERE message_id = ?",
            (message.id,),
        )
        db.commit()

    async def force(self, member: Member) -> bool:
        untrusted = member.guild.get_role(self.UNTRUSTED_ROLE_ID)
        if not untrusted:
            return False

        bot_member = member.guild.me
        removable_roles = [
            role
            for role in member.roles
            if not role.is_default()
            and role.id != untrusted.id
            and bot_member is not None
            and role < bot_member.top_role
        ]
        if removable_roles:
            await member.remove_roles(
                *removable_roles, reason="Removed due to forced verification"
            )
        await member.add_roles(untrusted, reason="Force verification")
        return True


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
