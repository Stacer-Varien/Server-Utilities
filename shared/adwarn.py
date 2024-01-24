from datetime import timedelta
from random import randint
from typing import List, Optional

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
from assets.functions import Warn
from config import hazead



class HAdropdown(ui.Select):
    def __init__(self, bot: Bot, member: Member, channel: TextChannel):
        self.bot = bot
        self.member = member
        self.channel = channel

        options = [
            SelectOption(label="Ad has an invalid invite"),
            SelectOption(label="Back-to-Back advertising"),
            SelectOption(label="Ad contains a public ping or mention"),
            SelectOption(label="Ad is an invite reward server"),
            SelectOption(label="NSFW ad, imagery or description"),
            SelectOption(label="Advertising in wrong channel"),
            SelectOption(label="Ad has short or no description"),
        ]

        super().__init__(
            placeholder="Which warning will the member recieve",
            min_values=1,
            max_values=1,
            options=options,
        )

    @staticmethod
    async def ha_warn(
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.channel.send(embed=failed_embed)
            return

        if member.bot:
            failed_embed = Embed(description="You can't warn a bot")
            await ctx.channel.send(embed=failed_embed)
            return

        warn_id = randint(0, 100000)
        embed = Embed(title="You were adwarned", color=0xFF0000)
        embed.add_field(name="Ad deleted in", value=channel.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)

        warn_data = Warn(member, ctx.user, warn_id)
        if warn_data.give(channel, reason):
            warn_data.give(channel, reason)
            warnpoints = warn_data.get_points()
            embed.add_field(name="Warn ID", value=warn_id, inline=True)
            embed.add_field(name="Warn Points", value=warnpoints, inline=True)

            punishment_actions = {
                3: (
                    "2hr",
                    "2 hour mute punishment applied",
                    "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied",
                ),
                6: (
                    None,
                    "Member has reached the 6 warn point punishment. A kick punishment was applied",
                ),
                10: (
                    None,
                    "Member has reached the 10 warn point punishment. A ban punishment was applied",
                ),
            }

            if warnpoints in punishment_actions:
                action = punishment_actions[warnpoints]
                if action[0] == "2hr":
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=2)),
                        reason="2 hour mute punishment applied",
                    )
                    result = action[2]
                    try:
                        timeout_msg = Embed(
                            description=f"You have received a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                        )
                        await member.send(embed=timeout_msg)
                    except:
                        pass
                elif action[0] is None:
                    if warnpoints == 6:
                        try:
                            kick_msg = Embed(
                                description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                            )
                            await member.send(embed=kick_msg)
                        except:
                            pass
                        await member.kick(reason="Kick punishment applied")
                    elif warnpoints == 10:
                        try:
                            ban_msg = Embed(
                                description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                            )
                            ban_msg.set_footer(
                                text="To appeal for your ban, join with this invite code: qZFhxyhTQh"
                            )
                            await member.send(embed=ban_msg)
                        except:
                            pass
                        await member.kick(reason="Kick punishment applied")
                    result = action[1]
                    embed.add_field(name="Result", value=result, inline=False)
            else:
                embed.add_field(
                    name="Result",
                    value="No warn point punishment applied",
                    inline=False,
                )

            embed.set_footer(
                text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
            )
            embed.set_thumbnail(url=member.display_avatar)
            m = await adwarn_channel.send(member.mention, embed=embed)
            msg = f"Warning sent. Check {m.jump_url}"
            await ctx.response.edit_message(msg)
            return

        await ctx.channel.send(
            f"Please wait <t:{warn_data.get_time()}:R> to adwarn the member"
        )

    async def callback(self, ctx: Interaction):
        await self.ha_warn(ctx, self.member, self.channel, self.values[0], None)


class HAdropdownView(ui.View):
    def __init__(self, bot: Bot, member: Member, channel: TextChannel):
        self.bot = bot
        self.member = member
        self.channel = channel
        super().__init__()

        self.add_item(HAdropdown(self.bot, self.member, self.channel))


class WarnCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.adwarn_context_menu = Serverutil.ContextMenu(
            name="Adwarn", callback=self.loa_adwarn_callback
        )
        self.bot.tree.add_command(self.adwarn_context_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.adwarn_context_menu.name, type=self.adwarn_context_menu.type
        )

    @Serverutil.guilds(hazead)
    @Serverutil.checks.has_any_role(
        919410986249756673,
        947109389855248504,
        749608853376598116,
        889019375988916264,
        849904285286006794,
        1136915107222401035,
        972072908065218560,
        1154076194837373021,
        849778145087062046,
        925790259319558159,
        925790259319558158,
        925790259319558157,
        1011971782426767390,
        925790259294396455,
    )
    async def loa_adwarn_callback(self, ctx: Interaction, message: Message) -> None:
        if ctx.guild.id == hazead:
            view = HAdropdownView(self.bot, message.author, message.channel)
        await ctx.response.defer(ephemeral=True)
        await message.delete()
        await ctx.followup.send(view=view)
        await view.wait()

    @staticmethod
    async def ha_warn(
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        adwarn_channel = ctx.guild.get_channel(925790260695281703)
        if member == ctx.user:
            failed_embed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed_embed)
            return

        if member.bot:
            failed_embed = Embed(description="You can't warn a bot")
            await ctx.followup.send(embed=failed_embed)
            return

        warn_id = randint(0, 100000)
        embed = Embed(title="You were adwarned", color=0xFF0000)
        embed.add_field(name="Ad deleted in", value=channel.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)

        warn_data = Warn(member, ctx.user, warn_id)
        if warn_data.give(channel, reason):
            warn_data.give(channel, reason)
            warnpoints = warn_data.get_points()
            embed.add_field(name="Warn ID", value=warn_id, inline=True)
            embed.add_field(name="Warn Points", value=warnpoints, inline=True)

            punishment_actions = {
                3: (
                    "2hr",
                    "2 hour mute punishment applied",
                    "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied",
                ),
                6: (
                    None,
                    "Member has reached the 6 warn point punishment. A kick punishment was applied",
                ),
                10: (
                    None,
                    "Member has reached the 10 warn point punishment. A ban punishment was applied",
                ),
            }

            if warnpoints in punishment_actions:
                action = punishment_actions[warnpoints]
                if action[0] == "2hr":
                    await member.edit(
                        timed_out_until=(utcnow() + timedelta(hours=2)),
                        reason="2 hour mute punishment applied",
                    )
                    result = action[2]
                    try:
                        timeout_msg = Embed(
                            description=f"You have received a timeout of 3 hours from **{ctx.guild.name}**\nYou have reached the 3 warn point punishment"
                        )
                        await member.send(embed=timeout_msg)
                    except:
                        pass
                elif action[0] is None:
                    if warnpoints == 6:
                        try:
                            kick_msg = Embed(
                                description=f"You are kicked from **{ctx.guild.name}**\nYou have reached the 6 warn point punishment"
                            )
                            await member.send(embed=kick_msg)
                        except:
                            pass
                        await member.kick(reason="Kick punishment applied")
                    elif warnpoints == 10:
                        try:
                            ban_msg = Embed(
                                description=f"You are banned from **{ctx.guild.name}**\nYou have reached the 10 warn point punishment"
                            )
                            ban_msg.set_footer(
                                text="To appeal for your ban, join with this invite code: qZFhxyhTQh"
                            )
                            await member.send(embed=ban_msg)
                        except:
                            pass
                        await member.kick(reason="Kick punishment applied")
                    result = action[1]
                    embed.add_field(name="Result", value=result, inline=False)
            else:
                embed.add_field(
                    name="Result",
                    value="No warn point punishment applied",
                    inline=False,
                )

            embed.set_footer(
                text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
            )
            embed.set_thumbnail(url=member.display_avatar)
            m = await adwarn_channel.send(member.mention, embed=embed)
            msg = f"Warning sent. Check {m.jump_url}"
            try:
                await ctx.response.edit_message(msg)
            except:
                await ctx.followup.send(msg, ephemeral=True)
            return

        await ctx.followup.send(
            f"Please wait <t:{warn_data.get_time()}:R> to adwarn the member"
        )



    @Serverutil.command(description="Adwarn someone for violating the ad rules")
    @Serverutil.checks.has_any_role(
        919410986249756673,
        947109389855248504,
        749608853376598116,
        889019375988916264,
        849904285286006794,
        1136915107222401035,
        972072908065218560,
        1154076194837373021,
        849778145087062046,
        925790259319558159,
        925790259319558158,
        925790259319558157,
        1011971782426767390,
        925790259294396455,
    )
    @Serverutil.describe(
        channel="Where was the ad deleted?",
        reason="What is the reason for the warn?",
        notes="Add notes if necessary",
    )
    async def adwarn(
        self,
        ctx: Interaction,
        member: Member,
        channel: TextChannel,
        reason: str,
        notes: Optional[str] = None,
    ):
        await ctx.response.defer()
        if ctx.guild.id == 925790259160166460:
            await self.ha_warn(ctx, member, channel, reason, notes)

    @adwarn.autocomplete("reason")
    async def autocomplete_callback(
        self, ctx: Interaction, current: str
    ) -> List[Serverutil.Choice[str]]:
        if ctx.guild.id == 925790259160166460:
            reasons = [
                "Ad has an invalid invite",
                "Back-to-Back advertising",
                "Ad contains a public ping or mention",
                "Ad is an invite reward server",
                "NSFW ad, imagery or description",
                "Advertising in wrong channel",
                "Ad has a short description",
                "Ad has a long description",
            ]
            return [
                Serverutil.Choice(name=reason, value=reason)
                for reason in reasons
                if current.lower() in reason.lower()
            ]

async def setup(bot: Bot):
    await bot.add_cog(WarnCog(bot), guild=Object(hazead))
