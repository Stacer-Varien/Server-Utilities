from datetime import datetime

from typing import List, Literal

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
from config import hazead


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
        adwarn=Adwarn()
        check_warn = adwarn.check_id(member, warn_id)
        if check_warn is None:
            await ctx.followup.send("Invalid warn ID", ephemeral=True)
            return
        
        await adwarn.remove(member, warn_id)

        embed = Embed(color=Color.green())
        embed.description = f"Your adwarn with Warn ID `{warn_id}` has been removed. You now have {adwarn.points(member)} points"
        adwarn_channel = await member.guild.fetch_channel(925790260695281703)
        m=await adwarn_channel.send(member.mention, embed=embed)

        await ctx.followup.send(
                "Warning revoked. Check {}".format(m.jump_url), ephemeral=True
            )




async def setup(bot: Bot):
    await bot.add_cog(AdwarnCog(bot), guild=Object(hazead))
