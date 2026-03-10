from discord import Message, PartialEmoji, TextChannel
from discord.ext.commands import Cog, Bot
from assets.functions import AutoMod
from config import vhf

class OnMessageCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        await AutoMod(self.bot, message).process_automod()

        if message.guild is None or message.guild.id != vhf:
            return

        categories = [
            1054090810800472154,
            985976523607650415,
            1194627560294842399,
            1194629375207952505,
            1165684137735241840,
            1194632735453630565,
        ]

        excluded_channel_ids = {
            1194722939342426306,
            1194723009563476089,
            1181566295540518992,
        }

        category_channel_ids = set()
        for category_id in categories:
            category = self.bot.get_channel(category_id)
            if category and hasattr(category, "channels"):
                category_channel_ids.update(ch.id for ch in category.channels)

        if message.channel.id not in category_channel_ids:
            return
        if message.channel.id in excluded_channel_ids:
            return

        if message.attachments:
            try:
                await message.add_reaction(
                    PartialEmoji(name="mhxaLove", id=1174261737697050625)
                )
            except Exception:
                pass
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
                if isinstance(message.channel, TextChannel) and message.channel.is_news():
                    await message.publish()


async def setup(bot: Bot):
    await bot.add_cog(OnMessageCog(bot))
