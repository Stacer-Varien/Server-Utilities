from datetime import timedelta
import datetime
from enum import Enum
from random import randint
from typing import List, Literal, Optional

from discord import (
    Color,
    Embed,
    Member,
    Interaction,
    Message,
    Object,
    TextChannel,
    app_commands as Serverutil,
    Forbidden,
    ui,
    SelectOption,
)
from discord.ext.commands import Cog, Bot
from discord.utils import utcnow
from assets.functions import Adwarn, Warn
from config import hazead


class AdwarnReasons(Enum):
    "Back-to-Back advertising", "Ad contains a public ping or mention", "Ad is an invite reward server", "NSFW ad, imagery or description", "Advertising in wrong channel"

class HAdropdown(ui.Select):
    def __init__(self, bot: Bot, member: Member, channel: TextChannel):
        self.bot = bot
        self.member = member
        self.channel = channel

        options = [
            SelectOption(label="Back-to-Back advertising"),
            SelectOption(label="Ad contains a public ping or mention"),
            SelectOption(label="Ad is an invite reward server"),
            SelectOption(label="NSFW ad, imagery or description"),
            SelectOption(label="Advertising in wrong channel"),
        ]

        super().__init__(
            placeholder="Which warning will the member recieve",
            min_values=1,
            max_values=1,
            options=options,
        )

    @staticmethod
    async def ha_adwarn(
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
    ):
        if member == ctx.user:
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed_embed, ephemeral=True)
            return

        if member.bot:
            failed_embed = Embed(description="You can't warn a bot")
            await ctx.followup.send(embed=failed_embed, ephemeral=True)
            return

        adwarn=Adwarn(ctx.user)
        current_time = round(datetime.now().timestamp())
        time = adwarn.check_time(member)
        if (current_time >= time) or (time == None):
            await Adwarn(ctx.user).add(member, channel, reason)
            await ctx
            return
        await ctx.followup.send(
            f"Please wait <t:{time}:R> to adwarn the member"
        )

    async def callback(self, ctx: Interaction):
        await self.ha_adwarn(ctx, self.member, self.channel, self.values[0])

class WarnCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role()
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
    )
    async def adwarn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: Literal[
            "Back-to-Back advertising",
            "Ad contains a public ping or mention",
            "Ad is an invite reward server",
            "NSFW ad, imagery or description",
            "Advertising in wrong channel",
        ],
    ):
        await ctx.response.defer(ephemeral=True)
        if member == ctx.user:
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed_embed, ephemeral=True)
            return

        if member.bot:
            failed_embed = Embed(description="You can't warn a bot")
            await ctx.followup.send(embed=failed_embed, ephemeral=True)
            return

        adwarn = Adwarn(ctx.user)
        current_time = round(datetime.now().timestamp())
        time = adwarn.check_time(member)
        if (current_time >= time) or (time == None):

            await Adwarn(ctx.user).add(member, channel, reason)
            await ctx.followup.send(
                "Adwarn sent. Check https://ptb.discord.com/channels/925790259160166460/925790260695281703"
            )
            return
        await ctx.followup.send(f"Please wait <t:{time}:R> to adwarn the member")

async def setup(bot: Bot):
    await bot.add_cog(WarnCog(bot), guild=Object(hazead))
