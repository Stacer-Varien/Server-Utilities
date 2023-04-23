from discord import Interaction, Object, app_commands
from discord.ext.commands import Cog, Bot
import traceback
from config import lss, hazead, orleans, loa


class errors(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.tree.on_error = self.on_app_command_error

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandInvokeError):
            traceback_error = traceback.format_exception(
                error, error, error.__traceback__
            )
            with open("errors.txt", "a") as f:
                f.writelines(f"{traceback_error}\n\n")

        try:
            thread = await ctx.guild.fetch_channel(1078749692457930842)
            await thread.send(f"```{traceback_error}```")
            await ctx.channel.send(
                "Well crap...\nAn error has happened but don't worry, its logged in {} so get ready for {} to scream his lungs out on this one :/".format(
                    thread.mention, str(self.bot.application.owner)
                )
            )
        except:
            return


async def setup(bot: Bot):
    await bot.add_cog(
        errors(bot),
        guilds=[Object(id=lss), Object(id=hazead), Object(id=orleans), Object(id=loa)],
    )
