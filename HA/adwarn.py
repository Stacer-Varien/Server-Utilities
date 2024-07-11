from datetime import datetime
from typing import Literal, Optional
from discord import (
    Color,
    Embed,
    Member,
    Interaction,
    Object,
    TextChannel,
    app_commands as Serverutil,
)
from discord.ext.commands import GroupCog, Bot
from assets.functions import Adwarn
from config import oad


class AdwarnCog(GroupCog, name="adwarn"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(
        925790259294396455,
        925790259319558154,
        1201835264964837408,
        1201835539310059520,
        925790259319558157,
        925790259319558158,
        925790259319558159,
    )
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
    )
    async def give(
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
        notes: Optional[Serverutil.Range[str, 3]] = None,
    ):
        await ctx.response.defer(ephemeral=True)

        if member == ctx.user:
            await ctx.followup.send(
                embed=Embed(description="You can't warn yourself"), ephemeral=True
            )
            return

        if member.bot:
            await ctx.followup.send(
                embed=Embed(description="You can't warn a bot"), ephemeral=True
            )
            return

        adwarn = Adwarn(ctx.user)
        current_time = round(datetime.now().timestamp())
        warn_time = adwarn.check_time(member)

        if warn_time is None or current_time >= warn_time:
            await adwarn.add(member, channel, reason, notes)
            await ctx.followup.send(
                "Adwarn sent. Check https://canary.discord.com/channels/925790259160166460/1239564619131912222",
                ephemeral=True,
            )
        else:
            await ctx.followup.send(
                f"Please wait <t:{warn_time}:R> to adwarn the member", ephemeral=True
            )

    @Serverutil.command(description="Remove an adwarn")
    @Serverutil.checks.has_any_role(
        1201835264964837408,
        1201835539310059520,
        925790259319558157,
        925790259319558158,
        925790259319558159,
    )
    @Serverutil.describe(
        warn_id="What is the warn ID?",
    )
    async def remove(self, ctx: Interaction, member: Member, warn_id: int):
        await ctx.response.defer(ephemeral=True)

        adwarn = Adwarn(ctx.user)
        if not adwarn.check_id(member, warn_id):
            await ctx.followup.send("Invalid warn ID", ephemeral=True)
            return

        await adwarn.remove(member, warn_id)

        embed = Embed(color=Color.green())
        embed.description = (
            f"Your adwarn with Warn ID `{warn_id}` has been removed. "
            f"You now have {adwarn.points(member)} points"
        )
        adwarn_channel = await member.guild.fetch_channel(1239564619131912222)
        message = await adwarn_channel.send(member.mention, embed=embed)

        await ctx.followup.send(
            f"Warning revoked. Check {message.jump_url}", ephemeral=True
        )


async def setup(bot: Bot):
    await bot.add_cog(AdwarnCog(bot), guild=Object(oad))
