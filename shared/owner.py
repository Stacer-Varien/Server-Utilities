import contextlib
from io import StringIO
from os import execv
from sys import executable, argv
from time import time

from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import is_owner
from nextcord.ext.commands import Cog, Bot

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


def restart_bot():
    execv(executable, ['python'] + argv)


class owner(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash(description="Changes the bot's play activity", guild_ids=[925790259160166460])
    @is_owner()
    async def activity(self, interaction: Interaction,
                       activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'],
                                                required=True),
                       activity=SlashOption(description="What is the new activity")):
        await interaction.response.defer()
        if activitytype == "listen":
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
            await interaction.followup.send(f"Bot's activity changed to `listening to {activity}`")
        elif activitytype == "play":
            await self.bot.change_presence(activity=Game(name=activity))
            await interaction.followup.send(f"Bot's activity changed to `playing {activity}`")

    @slash(description="Restart me to be updated", guild_ids=[925790259160166460])
    @is_owner()
    async def update(self, interaction: Interaction):
        await interaction.response.defer()
        msg:Message = await interaction.followup.send(f"Updating in 5 seconds!")
        await msg.delete()
        restart_bot()

    @slash(description="Evaluates a code")
    @is_owner()
    async def evaluate(self, ctx: Interaction, raw=SlashOption(choices=["True", "False"], required=False)):
        await ctx.response.defer()
        await ctx.followup.send("Insert your code.\nType 'cancel' if you don't want to evaluate")

        def check(m):
            return m.author == ctx.user and m.content

        code = await self.bot.wait_for('message', check=check)

        if code.content.startswith("cancel"):
            await ctx.edit_original_message(content="Evaluation aborted")
        elif code.content.startswith("```") and code.content.endswith("```"):
            str_obj = StringIO()
            start_time = time()
            try:
                with contextlib.redirect_stdout(str_obj):
                    exec(code.content.strip("`python"))
            except Exception as e:

                embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                              description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                end_time = time()
                embed.set_footer(
                    text=f"Compiled in {round((end_time - start_time) * 1000)}ms")
                return await ctx.followup.send(embed=embed)
            if raw == None:
                embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                               description=f'```{str_obj.getvalue()}```', color=0x008000)
                end_time = time()
                embed1.set_footer(
                    text=f"Compiled in {round((end_time - start_time) * 1000)}ms")
                await ctx.followup.send(embed=embed1)
            else:
                await ctx.followup.send(str_obj.getvalue())


def setup(bot: Bot):
    bot.add_cog(owner(bot))
