from discord import (
    Color,
    Embed,
    Interaction,
    Object,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog
from datetime import datetime
from assets.functions import LOAMod
from config import lss

class LOAmodCog(GroupCog, name="moderation"):
    def __init__(self, bot: Bot):
        self.bot = bot

    modgroup = Serverutil.Group(name="checks", description="...")

    @modgroup.command(
        name="stats",
        description="Check who has done the most ad moderations for the week",
    )
    @Serverutil.checks.has_role(1075400097615052900)
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
    )
    async def _reset(self, ctx: Interaction):
        await ctx.response.defer()
        if datetime.today().weekday <6:
            await ctx.followup.send(
                "DON'T RESET YET!\n\nYou can do a reset on {} to clear the database".format(
                    LOAMod().sunday.strftime("%d-%m-%Y")
                )
            )
            return

        LOAMod().reset_week()
        await ctx.followup.send("Moderator checks for last week have been reseted")

    @_stats.error
    async def _stats_error(
        self, ctx: Interaction, error: Serverutil.errors.AppCommandError
    ):
        if isinstance(error, Serverutil.errors.MissingAnyRole):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed)

    @_reset.error
    async def _reset_error(
        self, ctx: Interaction, error: Serverutil.errors.AppCommandError
    ):
        if isinstance(error, Serverutil.errors.MissingAnyRole):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed)


async def setup(bot: Bot):
    await bot.add_cog(LOAmodCog(bot), guild=Object(lss))
