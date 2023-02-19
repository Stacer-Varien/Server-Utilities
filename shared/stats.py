from datetime import timedelta
from sys import version_info as py_version
from time import time
from collections import OrderedDict
from json import load
from discord import Embed, Interaction, Color, Object
from discord import app_commands as Serverutil, __version__ as discord_version
from discord.ext.commands import Cog, Bot
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

    @Serverutil.command(
        description="See the bot's status from development to now")
    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        botowner = self.bot.get_user(597829930964877369)
        embed = Embed(title="Bot stats", color=Color.blue())
        embed.add_field(
            name="Developer",
            value=f"• **Name:** {botowner}\n• **ID:** {botowner.id}",
            inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Creation Date",
                        value=self.bot.user.created_at.strftime(format),
                        inline=True)
        embed.add_field(
            name="Version",
            value=
            f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n•**DiscordPy Version:** {discord_version}",
            inline=True)

        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = str(timedelta(seconds=difference))
        embed.add_field(name="Uptime", value=f"{uptime} hours", inline=True)

        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.set_footer(
            text=
            "I am the legacy version of the cousin bot, HazeBot developed by {}. If you wish to have a bot made by him, please DM him or email to **zane544yt@protonmail.com**. By the way, its not for free..."
            .format(botowner))
        await ctx.followup.send(embed=embed)

    @Serverutil.command(description="Check if a bot is made by Varien")
    async def validate_bot(self, ctx: Interaction, botid: str):
        await ctx.response.defer()
        f = open('assets/mybots.json')
        botowner = await self.bot.fetch_user(597829930964877369)
        bot = await self.bot.fetch_user(int(botid))
        if bot.bot == True:
            parms = OrderedDict([("%botowner%", str(botowner)),
                                 ("%bot%", str(bot)),
                                 ("%bot.id%", str(bot.id)),
                                 ("%botav%", bot.display_avatar)])
            try:

                json = load(replace_all(f, parms))

                embed = Embed.from_dict(json[botid]["embeds"][0])
            except KeyError:
                parms = OrderedDict([("%botowner", str(botowner)),
                                     ("%bot%", str(bot)),
                                     ("%bot.id%", str(bot.id)),
                                     ("%botav%", bot.display_avatar)])
                embed = Embed.from_dict(json["notmine"]["embeds"][0])
            await ctx.followup.send(embed=embed)
        else:
            await ctx.followup.send("This is a user account, not a bot account"
                                    )


def setup(bot: Bot):
    bot.add_cog(slashinfo(bot),
                guilds=[
                    Object(id=lss),
                    Object(id=hazead),
                    Object(id=orleans),
                    Object(loa)
                ])
