from datetime import datetime
from discord import Color, Embed, File, Interaction
from discord import app_commands as Serverutil
from discord.ext.commands import Bot, Cog, Context, NotOwner, CommandNotFound
import traceback
from io import BytesIO

class ErrorsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: Serverutil.AppCommandError
    ):
        if isinstance(error, Serverutil.MissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.channel.send(embed=embed)

        elif isinstance(error, Serverutil.BotMissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.channel.send(embed=embed)

        elif isinstance(error, Serverutil.errors.CommandInvokeError):
            traceback_error = traceback.format_exception(
                error, error, error.__traceback__
            )

            trace="".join(traceback_error)
            
            with open("errors.txt", "a") as f:
                f.writelines(f"{datetime.now()} --- {trace}")
            
            file=BytesIO(trace.encode("utf-8"))
            file=File(file, filename="error.txt")
            
            channel = await self.bot.fetch_channel(1169726260533018644)
            await channel.send(file=file)
        elif isinstance(error, Serverutil.errors.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.channel.send(embed=embed)


        elif isinstance(error, Serverutil.CommandOnCooldown):
            pass



    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, NotOwner):
            return


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
