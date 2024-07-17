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
                            ]:
                                await message.publish()
                                return

            ha = await self.bot.fetch_guild(925790259160166460)

            if (message.guild == ha and message.channel.id):
                categories_ha = [
                    1239493037693075467,
                    1239493114842972242,
                    1239493175828152482,
                ]
                ha_ad_channels = [
                    channel
                    for category_id in categories_ha
                    for channel in self.bot.get_channel(category_id).channels
                ]
                for channel in ha_ad_channels:
                    if channel.id not in [
                        1240196579466412052,
                        1239569790947819622,
                    ]:
                        await Currency(message.author).add_credits(2)
                        if datetime.today().weekday() >= 5:
                            await Currency(message.author).add_credits(3)
                        await message.add_reaction(":HAZECoin:")
                        return        


async def setup(bot: Bot):
    await bot.add_cog(OnMessageCog(bot))
