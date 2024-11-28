from datetime import datetime
from discord import Message, TextChannel
from discord.ext.commands import Cog, Bot
from assets.functions import AutoMod, Currency
from assets import ad_chan_rules

class OnMessageCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            await AutoMod(self.bot, message).process_automod()
            if message.guild.id==974028573893595146:
                categories = [
                    1054090810800472154,
                    985976523607650415,
                    1194627560294842399,
                    1194629375207952505,
                    1165684137735241840,
                    1194632735453630565,
                ]

                starboard_cats = [
                    channel
                    for category_id in categories
                    for channel in self.bot.get_channel(category_id).channels
                ]

                for channel in starboard_cats:
                    if channel.id not in [
                        1194722939342426306,
                        1194723009563476089,
                        1181566295540518992,
                    ]:

                        if len(message.attachments) >= 1:
                            await message.add_reaction(":mhxaLove:1174261737697050625")
                            if message.channel.id in [
                                1115726593457926294,
                                1003589695910973480,
                                1110173625778196581,
                                1054091901852209252,
                                1054091728816181328,
                                1054091953433747539,
                                1082393894190321835,
                                1179067756918882386,
                            ]:
                                await message.publish()
                                return 


async def setup(bot: Bot):
    await bot.add_cog(OnMessageCog(bot))
