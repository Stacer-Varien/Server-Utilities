from discord import (
    Embed,
    Interaction,
    Member,
    Object,
    TextChannel,
    app_commands as Serverutil,
)
from discord.ext.commands import Cog, Bot
from config import hazead
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.functions import Warn

class warncog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def warn_message(
        self, ctx: Interaction, member: Member, channel: TextChannel, reason: str
    ):
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)

        else:
            embed = Embed()
            warn_id = randint(0, 100000)
            embed = Embed(title="You have been warned", color=0xFF0000)
            embed.add_field(name="Ad deleted in", value=channel.mention, inline=False)
            embed.add_field(name="Reason for warn", value=reason, inline=False)

            warn_data = Warn(member, ctx.user, warn_id)
            if warn_data.give(channel, reason) == False:
                return await ctx.followup.send(
                    f"The member was warned recently. Please wait after <t:{warn_data.get_time()}:t>"
                )
            else:
                warn_data.give(channel, reason)
                warnpoints = warn_data.get_points()
                embed.add_field(name="Warn ID", value=warn_id, inline=True)
                embed.add_field(name="Warn Points", value=warnpoints, inline=True)

                if warnpoints == 3:
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=2)),
                        reason="2 hour mute punishment applied",
                    )
                    result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"

                    try:
                        timeoutmsg = Embed(
                            description=f"You have recieved a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                        )
                        await member.send(embed=timeoutmsg)
                    except:
                        pass

                elif warnpoints == 6:
                    try:
                        kickmsg = Embed(
                            description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                        )
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                elif warnpoints == 10:
                    try:
                        banmsg = Embed(
                            description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                        )
                        banmsg.set_footer(
                            text="To appeal for your ban, join with this invite code: qZFhxyhTQh"
                        )
                        await member.send(embed=banmsg)
                    except:
                        pass
                    await member.kick(reason="Kick punishment applied")
                    result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                else:
                    result = "No warn point punishment applied"

                    embed.add_field(name="Result", value=result, inline=False)
                    embed.set_footer(
                        text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
                    )
                    embed.set_thumbnail(url=member.display_avatar)
                    await adwarn_channel.send(member.mention, embed=embed)
                    await ctx.followup.send(
                        f"Warning sent. Check {adwarn_channel.mention}", ephemeral=True
                    )

    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(925790259294396455, 925790259319558154, 1011971782426767390, 925790259319558157, 925790259319558158, 925790259319558159)
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?")
    async def adwarn(
        self, ctx: Interaction, member: Member, channel: TextChannel, reason: str
    ):
        await ctx.response.defer()

        await self.warn_message(ctx, member, channel, reason)


async def setup(bot: Bot):
    await bot.add_cog(warncog(bot), guild=Object(hazead))
