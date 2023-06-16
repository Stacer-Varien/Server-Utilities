from datetime import timedelta
from sys import version_info as py_version
from time import time
from collections import OrderedDict
from json import loads
from discord import Embed, Interaction, Color, Object
from discord import app_commands as Serverutil, __version__ as discord_version
from discord.ext.commands import Cog, Bot, GroupCog
from config import lss, hazead, loa, orleans

format = "%a, %d %b %Y | %H:%M:%S"
start_time = time()


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class slashinfo(Cog):
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
            value=self.bot.user.created_at.strftime(format),
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
            text="I am the legacy version of the cousin bot, HazeBot developed by {}. If you wish to have a bot made by him, please DM him or email to **zane544yt@protonmail.com**. By the way, its not for free...".format(
                botowner
            )
        )
        await ctx.followup.send(embed=embed)

    @Serverutil.command(description="Check if a bot is made by Varien")
    async def validate_bot(self, ctx: Interaction, botid: str):
        await ctx.response.defer()
        with open("assets/mybots.json", "r") as f:
            content = "".join(f.readlines())
        if int(botid) == 1067838201185706056:
            pass
        else:
            bot = await self.bot.fetch_user(int(botid))
        botowner = await self.bot.fetch_user(597829930964877369)

        parms = OrderedDict(
            [
                ("%botowner%", str(botowner)),
                ("%bot%", str(bot)),
                ("%bot.id%", str(bot.id)),
                ("%botav%", str(bot.display_avatar)),
            ]
        )
        if bot.bot == True:
            try:
                json = loads(replace_all(content, parms))

                embed = Embed.from_dict(json[botid]["embeds"][0])
            except KeyError:
                json = loads(replace_all(content, parms))
                embed = Embed.from_dict(json["notmine"]["embeds"][0])
            await ctx.followup.send(embed=embed)
        else:
            await ctx.followup.send("This is a user account, not a bot account")


class botpro(GroupCog, name="bot"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(name="tos", description="View the ToS of Server Utilities")
    async def tos(self, ctx: Interaction):
        embed = Embed()
        embed.color = Color.random()
        embed.title = "Terms of Service when using Server Utilities"
        embed.description = """
**Use of Alt Accounts**
There is no limits to the use of alt accounts. However, using them to try and break the bot in some way is not allowed.

**Defamation and Reputational Harm**
Spreading rumours and false reports about Server Utilities (such as calling it a nuke bot), causing unwanted drama or attacking me or Server Utilities is punishable.

**Buying Server Utilities**
Under no circumstances, Server Utilities (including its token) is not for sale.

**Adding Server Utilities**
Server Utilities, under no condition by a 3rd party, is not up for grabs or free to have. The bot is ONLY for my servers including LOA and LSS (it was added conditionally)

**Copyright**
Even though Server Utilities's repository is public and free to use for educational and/or experimental purposes, you are not allowed to impersonate it and/or sell the source code as it is under a Conditioned MIT License and Common Clause License. (To learn more about the Licenses, please use `/bot license`)
        """
        await ctx.response.send_message(embed=embed, delete_after=180)

    @Serverutil.command(name="license", description="View the licenses of the bot")
    async def license(sefl, ctx: Interaction):
        content = """
Conditioned MIT License

Copyright (c) 2022 Stacer-Varien

Permission is hereby granted, free of charge, to any person obtaining a copy
of Server Utilities and associated documentation files, to deal
in the bot without restriction, including without limitation the rights
to use, modify, merge, and to permit persons to whom the bot is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in
all copies or substantial portions of Server Utilities.

2. The bot and/or source code should not be copied and claimed by its own by the 3rd party.

3. The bot should not be the same as the original bot.

4. The bot and/or it's source code should not be sold to anyone in any way or form.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


“Commons Clause” License Condition v1.0

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

License: Conditioned MIT License

Licensor: Stacer-Varien
"""

        embed = Embed()
        embed.color = Color.random()
        embed.title = "Server Utilities' Licenses"
        embed.description = content

        await ctx.response.send_message(embed=embed, delete_after=180)


async def setup(bot: Bot):
    await bot.add_cog(
        slashinfo(bot),
        guilds=[Object(id=lss), Object(id=hazead), Object(id=orleans), Object(id=loa)],
    )
    await bot.add_cog(
        botpro(bot),
        guilds=[Object(id=lss), Object(id=hazead), Object(id=orleans), Object(id=loa)],
    )
