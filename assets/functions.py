from typing import Optional

from discord import (
    HTTPException,
    Member,
    Message,
)
from discord.ext.commands import Bot
from config import db


class AutoMod:
    def __init__(self, bot: Bot, message: Message):
        self.bot = bot
        self.message = message

    async def process_automod(self) -> bool:
        if self.message.guild is None:
            return False

        content = self.message.content
        channel_id = self.message.channel.id

        if any(
            url in content.lower() for url in ("discord.gg/", "discord.com/invite/")
        ) and channel_id not in [
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

    async def check_invite(self, invite_url: str, check_blacklist=False):
        try:
            invite = await self.bot.fetch_invite(invite_url)

            if (
                check_blacklist
                and invite.guild
                and invite.guild.id in await self.get_blacklisted_servers()
            ):
                await self.handle_blacklisted_server()
                return

        except HTTPException:
            return

    async def handle_blacklisted_server(self):
        await self.delete_message()

    async def get_blacklisted_servers(self):
        return await db.get_blacklisted_server_ids()


class Verification:
    VERIFY_ROLE_ID = 974760640742825984
    MEMBER_ROLE_ID = 974760599487647815
    UNTRUSTED_ROLE_ID = 974760534102650950

    def __init__(self) -> None:
        pass

    async def add_request(self, member: Member, message: Message):
        await db.add_verification_request(member.id, message.id)

    async def get_request_member(self, message: Message) -> Optional[Member]:
        if message.guild is None:
            return None
        user_id = await self.get_request_user_id(message)
        return message.guild.get_member(user_id) if user_id else None

    async def get_request_user_id(self, message: Message) -> Optional[int]:
        return await db.get_request_user_id(message.id)

    async def check_user(self, message: Message) -> Optional[Member]:
        return await self.get_request_member(message)

    async def has_request_for_message(self, message: Message) -> bool:
        return await db.has_request_for_message(message.id)

    async def has_request_for_member(self, member: Member) -> bool:
        return await db.has_request_for_user(member.id)

    def is_verified(self, member: Member) -> bool:
        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)
        return bool(verify_role and verify_role in member.roles)

    async def check(self, message: Message) -> bool:
        return await self.has_request_for_message(message)

    async def approve(self, message: Message, member: Optional[Member] = None):
        member = member or await self.get_request_member(message)
        if not member:
            return

        verify_role = member.guild.get_role(self.VERIFY_ROLE_ID)
        member_role = member.guild.get_role(self.MEMBER_ROLE_ID)
        untrusted = member.guild.get_role(self.UNTRUSTED_ROLE_ID)

        if verify_role is None:
            raise RuntimeError("The configured verification role does not exist.")

        await member.add_roles(verify_role, reason="Successfully verified")

        if untrusted and untrusted in member.roles:
            await member.remove_roles(
                untrusted, reason="Successful forced verification"
            )
            if member_role:
                await member.add_roles(member_role, reason="Add member role")

        await self.remove_request(message)

    async def deny(self, message: Message):
        await self.remove_request(message)

    async def remove_request(self, message: Message):
        await db.remove_verification_request(message.id)

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

    async def get_blacklisted_servers(self):
        return await db.get_blacklisted_server_ids()

    async def add(self, server_id: str, reason: str):
        await db.add_blacklisted_server(int(server_id), reason)

    async def remove(self, server_id: str):
        await db.remove_blacklisted_server(int(server_id))
