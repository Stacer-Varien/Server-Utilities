from typing import Optional
from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Object,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog, Cog
from datetime import datetime, timedelta
from discord.utils import utcnow
from humanfriendly import InvalidTimespan, parse_timespan, format_timespan
from assets.functions import LOAMod
from config import loa, lss


class LOAmodCog(GroupCog, name="moderation"):
    def __init__(self, bot: Bot):
        self.bot = bot

    modgroup = Serverutil.Group(name="check", description="...")

    @modgroup.command(name="cooldowns")
    @Serverutil.checks.has_any_role(1154076194837373021)
    async def _cooldowns(self, ctx: Interaction):
        embed = Embed()
        if ctx.channel.id == 954594959074418738:
            await ctx.response.defer()
            embed.color = Color.blue()
            data = LOAMod()._cooldowns()
            if data == None:
                embed.description = "No cooldowns available"
            else:
                cooldowns = []
                for i in data:
                    try:
                        user = await ctx.guild.fetch_member(int(i[0]))
                        cooldown = f"<t:{i[2]}:R>"
                        cooldowns.append(f"{user} | {cooldown}\n")
                    except:
                        continue
                embed.title = "User | Cooldown"
                embed.description = "".join(cooldowns)
                embed.set_footer(
                    text="If the cooldown time says 'in x time', that means you have to wait until the member can be adwarned"
                )

            await ctx.followup.send(embed=embed)
            return
        embed.description = "Please use this command in https://ptb.discord.com/channels/704888699590279221/954594959074418738"
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @modgroup.command(
        name="stats",
        description="Check who has done the most ad moderations for the week",
    )
    @Serverutil.checks.has_any_role(
        1075400097615052900, 1160572350761279548, 1160568155807154296
    )
    async def _stats(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.blue())
        embed.description = await LOAMod().checks(self.bot)
        embed.set_footer(
            text="If a moderator's name is not there, they have not commited an adwarn command."
        )
        await ctx.followup.send(embed=embed)

    @modgroup.command(name="reset", description="Resets last week's checks")
    @Serverutil.checks.has_any_role(
        1074770189582872606,
        1074770253294342144,
        1074770323293085716,
        1076650317392916591,
        949147509660483614,
        1160568155807154296,
    )
    async def _reset(self, ctx: Interaction):
        await ctx.response.defer()
        if datetime.today().weekday < 6:
            await ctx.followup.send(
                "DON'T RESET YET!\n\nYou can do a reset on a Sunday to clear the database".format()
            )
            return

        LOAMod().reset_week()
        await ctx.followup.send("Moderator checks for last week have been reseted")


class ModCog2(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Serverutil.command(description="Put a member on timeout")
    @Serverutil.checks.has_permissions(moderate_members=True)
    @Serverutil.describe(
        member="Which member?",
        time="How long should they be on timeout (1m, 1h30m, etc)",
        reason="Why are they on timeout?",
    )
    async def timeout(
        self,
        ctx: Interaction,
        member: Member,
        reason: Serverutil.Range[str, None, 470] = None,
        time: Optional[str] = None,
    ) -> None:
        adwarn_channel = await ctx.guild.fetch_channel(745107170827305080)
        if ctx.channel.id == 954594959074418738:
            await ctx.response.defer()

            if member == ctx.user:
                failed = Embed(description="You can't time yourself out")
                await ctx.followup.send(embed=failed)
                return

            if not time or (parse_timespan(time) > 2505600.0):
                time = "28d"

            timed = parse_timespan(time)
            await member.edit(
                timed_out_until=utcnow() + timedelta(seconds=timed),
                reason="{} | {}".format(reason, ctx.user),
            )
            mute = Embed(title=":warning: You have been put on timeout", color=0xFF0000)
            mute.add_field(
                name=":shield: Moderator",
                value=ctx.user,
                inline=False,
            )
            mute.add_field(
                name=":timer: Duration", value=format_timespan(timed), inline=False
            )
            mute.add_field(name=":bell: Reason", value=reason, inline=False)
            mute.set_thumbnail(url=member.display_avatar)
            m = await adwarn_channel.send(embed=mute)
            muted = Embed(
                description=f"{member} has been put on timeout. Check {m.jump_url}",
                color=0xFF0000,
            )
            await ctx.followup.send(member.mention, embed=muted)
            LOAMod(ctx.user).add_mod_point()
            return

        await ctx.response.send_message(
            embed=Embed(
                description=f"Please use the command in {adwarn_channel.jump_url}",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @timeout.error
    async def timeout_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.CommandInvokeError) and isinstance(
            error.original, InvalidTimespan
        ):
            embed = Embed()
            embed.description = "Invalid time added. Please try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Serverutil.command(description="Removes a member from timeout")
    @Serverutil.describe(member="Which member?", reason="Why are they untimeouted?")
    @Serverutil.checks.has_permissions(moderate_members=True)
    @Serverutil.checks.bot_has_permissions(moderate_members=True)
    async def untimeout(
        self,
        ctx: Interaction,
        member: Member,
        reason: Serverutil.Range[str, None, 470] = None,
    ) -> None:
        adwarn_channel = await ctx.guild.fetch_channel(745107170827305080)
        if ctx.channel.id == 954594959074418738:
            await ctx.response.defer()
            if member == ctx.user:
                failed = Embed(description="You can't untime yourself out")
                await ctx.followup.send(embed=failed)
                return

            await member.edit(
                timed_out_until=None, reason="{} | {}".format(reason, ctx.user)
            )
            unmute = Embed(title="Your timeout has been removed", color=0xFF0000)
            unmute.add_field(
                name=":shield: Moderator",
                value=ctx.user,
                inline=True,
            )
            unmute.add_field(name=":bell: Reason", value=reason, inline=False)
            unmute.set_thumbnail(url=member.display_avatar)

            m = await adwarn_channel.send(embed=unmute)
            unmuted = Embed(
                description=f"{member} has been untimeouted. Check {m.jump_url}",
                color=0xFF0000,
            )

            await ctx.followup.send(member.mention, embed=unmuted)
            return
        await ctx.response.send_message(
            embed=Embed(
                description=f"Please use the command in {adwarn_channel.jump_url}",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Serverutil.command(description="Ban someone in this server")
    @Serverutil.describe(
        member="Which member are you banning?",
        reason="What did they do?",
    )
    @Serverutil.checks.has_permissions(ban_members=True)
    @Serverutil.checks.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: Interaction,
        member: Member,
        reason: Serverutil.Range[str, None, 450] = None,
    ) -> None:
        adwarn_channel = await ctx.guild.fetch_channel(745107170827305080)
        if ctx.channel.id == 954594959074418738:
            if member == ctx.user:
                failed = Embed(description="You can't ban yourself")
                await ctx.followup.send(embed=failed)
                return

            if member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You can't ban the owner of the server...",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=failed)
                return

            if ctx.user.top_role.position < member.top_role.position:
                failed = Embed(
                    description="{}'s position is higher than you...".format(member),
                    color=Color.red(),
                )
                await ctx.followup.send(embed=failed)
                return

            try:
                banmsg = Embed(
                    description=f"You are banned from **{ctx.guild.name}** for **{reason}**"
                )
                await member.send(embed=banmsg)
            except:
                pass

            await member.ban(reason="{} | Banned by {}".format(reason, ctx.user))

            ban = Embed(
                title=f"Member Banned from **{ctx.guild.name}**", color=0xFF0000
            )
            ban.add_field(
                name=":shield: Moderator",
                value=ctx.user,
                inline=True,
            )
            ban.add_field(name=":bell: Reason", value=reason, inline=False)
            ban.set_thumbnail(url=member.display_avatar)

            m = await adwarn_channel.send(embed=ban)

            banned = Embed(
                description=f"{member} has been banned. Check {m.jump_url}",
                color=0xFF0000,
            )
            await ctx.followup.send(embed=banned)
            LOAMod(ctx.user).add_mod_point()
            return
        await ctx.response.send_message(
            embed=Embed(
                description=f"Please use the command in {adwarn_channel.jump_url}",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Serverutil.command(description="Kick a member out of the server")
    @Serverutil.describe(
        member="Which member are you kicking?", reason="Why are they being kicked?"
    )
    @Serverutil.checks.has_permissions(kick_members=True)
    @Serverutil.checks.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: Interaction,
        member: Member,
        reason: Serverutil.Range[str, None, 450] = None,
    ) -> None:
        adwarn_channel = await ctx.guild.fetch_channel(745107170827305080)
        if ctx.channel.id == 954594959074418738:
            if member.id == ctx.user.id:
                failed = Embed(description="You can't kick yourself out")
                await ctx.followup.send(embed=failed)
                return
            if ctx.user.top_role.position < member.top_role.position:
                failed = Embed(
                    description="{}'s position is higher than you...".format(member),
                    color=Color.red(),
                )
                await ctx.followup.send(embed=failed)
                return
            if member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You cannot kick the owner of the server out...",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=failed)
                return
            if member == ctx.user:
                failed = Embed(description="You can't kick yourself out")
                await ctx.followup.send(embed=failed)
                return

            try:
                kickmsg = Embed(
                    description=f":boot: You are kicked from **{ctx.guild.name}** for **{reason}**"
                )
                await member.send(embed=kickmsg)
            except:
                pass

            # await member.kick(reason="{} | {}".format(reason, ctx.user))
            await ctx.guild.kick(
                member, reason="{} | Kicked by {}".format(reason, ctx.user)
            )
            kick = Embed(
                title=f":boot: Member kicked from {ctx.guild.name}", color=0xFF0000
            )
            kick.add_field(
                name=":bust_in_silhouette: Member", value=member, inline=True
            )
            kick.add_field(
                name=":shield: Moderator",
                value=ctx.user,
                inline=True,
            )
            kick.add_field(name=":bell: Reason", value=reason, inline=True)
            kick.set_thumbnail(url=member.display_avatar)

            m = await adwarn_channel.send(embed=kick)

            kicked = Embed(
                description=f"{member} has been kicked. Check {m.jump_url}",
                color=0xFF0000,
            )

            await ctx.followup.send(embed=kicked)
            return
        await ctx.response.send_message(
            embed=Embed(
                description=f"Please use the command in {adwarn_channel.jump_url}",
                color=Color.red(),
            ),
            ephemeral=True,
        )


async def setup(bot: Bot):
    await bot.add_cog(LOAmodCog(bot), guilds=[Object(lss), Object(loa)])
    await bot.add_cog(ModCog2(bot), guild=Object(loa))
