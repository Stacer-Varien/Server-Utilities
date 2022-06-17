from asyncio import sleep
import contextlib
from io import StringIO
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as slash
from os import execv
from sys import executable, argv
from nextcord.ext.application_checks import is_owner

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


def restart_bot():
  execv(executable, ['python'] + argv)


class evaluatecog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description="Changes the bot's play activity")
    @is_owner()
    async def activity(self, interaction: Interaction, activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'], required=True), activity=SlashOption(description="What is the new activity")):
        await interaction.response.defer()
        if activitytype == "listen":
                await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
                await interaction.followup.send(f"Bot's activity changed to `listening to {activity}`")
        elif activitytype == "play":
            await self.bot.change_presence(activity=Game(name=activity))
            await interaction.followup.send(f"Bot's activity changed to `playing {activity}`")

    @slash(description="Restart me to be updated")
    @is_owner()
    async def update(self, interaction: Interaction):
        await interaction.response.defer()
        msg = await interaction.followup.send(f"Updating in 5 seconds!")
        await sleep(5)
        await msg.delete()
        restart_bot()

    @slash(description="Evaluates a code")
    @is_owner()
    async def evaluate(self, interaction: Interaction):
            await interaction.response.defer()
            await interaction.followup.send('Insert your code')

            def check(m):
                    return m.author == interaction.user and m.content

            code = await self.bot.wait_for('message', check=check)

            str_obj = StringIO()
            try:
                    with contextlib.redirect_stdout(str_obj):
                        exec(code.content)
            except Exception as e:
                    embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                                  description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                    embed.set_footer(
                        text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                    return await interaction.followup.send(embed=embed)
            embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                               description=f'```{str_obj.getvalue()}```', color=0x008000)
            embed1.set_footer(
                    text=f"Compiled in {round(self.bot.latency * 1000)}ms")
            await interaction.followup.send(embed=embed1)


def setup(bot):
    bot.add_cog(evaluatecog(bot))
