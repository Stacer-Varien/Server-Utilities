from collections import OrderedDict
from datetime import timedelta
from json import loads
from sys import version_info as py_version
from time import time
from discord import app_commands as Serverutil, __version__ as discord_version
from discord import Embed, Interaction, Color
from discord.ext.commands import Cog, Bot, GroupCog


start_time = time()


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class InfoCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="See the bot's status from development to now")
    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        botowner = self.bot.application.owner
        embed = Embed(title="Bot stats", color=Color.blue())
        embed.add_field(
            name="Developer",
            value=f"• **Name:** {str(botowner)}\n• **ID:** {botowner.id}",
            inline=True,
        )
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(
            name="Creation Date",
            value=f"<t:{round(self.bot.user.created_at.timestamp())}:F>",
            inline=True,
        )
        embed.add_field(
            name="Version",
            value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n•**DiscordPy Version:** {discord_version}",
            inline=True,
        )

        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = str(timedelta(seconds=difference))
        embed.add_field(name="Uptime", value=f"{uptime} hours", inline=True)

        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.set_footer(
            text="I am the legacy version of the cousin bot, HazeBot developed by {}. If you wish to have a bot made by him, please DM him or email to `jeannebot.discord@gmail.com`. By the way, its not for free...".format(
                botowner
            )
        )
        await ctx.followup.send(embed=embed)


class BotTosCog(GroupCog, name="bot"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(name="tos", description="View the ToS of Server Utilities")
    async def tos(self, ctx: Interaction):
        embed = Embed()
        embed.color = Color.random()
        embed.title = "Terms of Service when using Server Utilities"
        embed.description = """
**Defamation and Reputational Harm**
Spreading rumours and false reports about Server Utilities (such as calling it a nuke bot), causing unwanted drama or attacking me or Server Utilities is punishable.

**Buying Server Utilities**
Under no circumstances, Server Utilities (including its token) is not for sale.

**Adding Server Utilities**
Server Utilities is not up for grabs or free to have. The bot is ONLY for **my** servers. Add my bot, [Jeanne](https://top.gg/bot/831993597166747679) instead

**Copyright**
Even though Server Utilities's repository is public and free to use for educational and/or experimental purposes, you are not allowed to impersonate it and/or sell the source code as it is under a MIT License and Common Clause License. (To learn more about the Licenses, please use `/bot license`)
        """
        await ctx.response.send_message(embed=embed, delete_after=180)

    @Serverutil.command(name="license", description="View the licenses of the bot")
    async def license(self, ctx: Interaction):
        content = """

# MIT License
Copyright 2022 Stacer-Varien

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# “Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined 
below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under 
the License will not include, and the License does not grant to you, the right
to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights 
granted to you under the License to provide to third parties, for a fee or other 
consideration (including without limitation fees for hosting or consulting/ support 
services related to the Software), a product or service whose value derives, entirely 
or substantially, from the functionality of the Software. Any license notice or 
attribution required by the License must also include this Commons Clause License 
Condition notice.

Software: Server Utilities

License: MIT License

Licensor: Stacer-Varien
"""

        embed = Embed()
        embed.color = Color.random()
        embed.title = "Server Utilities' Licenses"
        embed.description = content

        await ctx.response.send_message(embed=embed, delete_after=180)


async def setup(bot: Bot):
    await bot.add_cog(InfoCog(bot))
    await bot.add_cog(BotTosCog(bot))
