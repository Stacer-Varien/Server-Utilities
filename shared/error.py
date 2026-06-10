import logging

from discord import Color, Embed, HTTPException, Interaction
from discord import app_commands as Serverutil
from discord.ext.commands import (
    Bot,
    CheckFailure,
    Cog,
    CommandNotFound,
    CommandOnCooldown,
    Context,
    NotOwner,
    UserInputError,
)

logger = logging.getLogger(__name__)


class ErrorsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        self.bot.tree.on_error = self._old_tree_error

    async def send_app_error(self, ctx: Interaction, description: str):
        embed = Embed(description=description, color=Color.red())
        try:
            if ctx.response.is_done():
                await ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.response.send_message(embed=embed, ephemeral=True)
        except HTTPException:
            logger.warning("Could not send error response for interaction %s", ctx.id)

    async def on_app_command_error(
        self, ctx: Interaction, error: Serverutil.AppCommandError
    ):
        if isinstance(
            error,
            (
                Serverutil.MissingPermissions,
                Serverutil.BotMissingPermissions,
                Serverutil.NoPrivateMessage,
                Serverutil.MissingAnyRole,
                Serverutil.MissingRole,
            ),
        ):
            await self.send_app_error(ctx, str(error))
            return

        if isinstance(error, Serverutil.CommandOnCooldown):
            await self.send_app_error(
                ctx, f"You're on cooldown. Try again in {error.retry_after:.1f}s."
            )
            return

        original = getattr(error, "original", error)
        logger.error(
            "Unhandled app command error in %s",
            getattr(ctx.command, "qualified_name", "unknown command"),
            exc_info=(type(original), original, original.__traceback__),
        )
        await self.send_app_error(
            ctx,
            "Something went wrong while running that command. The error was logged.",
        )

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, (CommandNotFound, NotOwner)):
            return

        if isinstance(error, CommandOnCooldown):
            await ctx.send(
                f"You're on cooldown. Try again in {error.retry_after:.1f}s."
            )
            return

        if isinstance(error, (UserInputError, CheckFailure)):
            await ctx.send(str(error))
            return

        original = getattr(error, "original", error)
        logger.error(
            "Unhandled prefix command error in %s",
            getattr(ctx.command, "qualified_name", "unknown command"),
            exc_info=(type(original), original, original.__traceback__),
        )
        await ctx.send("Something went wrong while running that command.")


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
