from datetime import timedelta
from sys import version_info as py_version
from time import time

from nextcord import *
from nextcord import slash_command as slash, __version__ as discord_version
from nextcord.ext.commands import Cog

format = "%a, %d %b %Y | %H:%M:%S"
start_time = time()


class slashinfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description="See the bot's status from development to now")
    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        botowner = self.bot.get_user(597829930964877369)
        embed = Embed(title="Bot stats", color=Color.blue())
        embed.add_field(
            name="Developer", value=f"• **Name:** {botowner}\n• **ID:** {botowner.id}", inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Creation Date", value=self.bot.user.created_at.strftime(
            format), inline=True)
        embed.add_field(
            name="Version",
            value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n•**Nextcord Version:** {discord_version}",
            inline=True)

        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = str(timedelta(seconds=difference))
        embed.add_field(
            name="Uptime", value=f"{uptime} hours", inline=True)

        embed.set_thumbnail(
            url=self.bot.user.avatar)
        embed.set_footer(
            text="I am the legacy version of the cousin bot, HazeBot developed by {}. If you wish to have a bot made by him, please DM him. By the way, its not for free...".format(
                botowner))
        await ctx.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(slashinfo(bot))
