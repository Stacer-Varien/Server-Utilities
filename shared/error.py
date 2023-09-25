import traceback

from discord import (
    Interaction,
    Object,
    app_commands,
    NotFound,
    Forbidden,
    HTTPException,
)
from discord.ext.commands import Cog, Bot

from config import lss, hazead, orleans, loa


class Errors(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.on_app_command_error = self.on_app_command_error

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            # noinspection PyTypeChecker
            traceback_error = traceback.format_exception(
                error, error, error.__traceback__
            )
            with open("errors.txt", "a") as f:
                f.writelines("".join(traceback_error))

        try:
            thread = await self.bot.fetch_channel(1078749692457930842)
            await thread.send(f"```{''.join(traceback_error)}```")
        except (NotFound, Forbidden, HTTPException):
            return


async def setup(bot: Bot):
    await bot.add_cog(
        Errors(bot),
        guilds=[Object(id=lss), Object(id=hazead), Object(id=orleans), Object(id=loa)],
    )
