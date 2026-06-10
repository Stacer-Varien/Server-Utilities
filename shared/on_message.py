from discord import HTTPException, Message, PartialEmoji, TextChannel
from discord.ext.commands import Cog, Bot
from assets.functions import AutoMod
from config import vhf


class OnMessageCog(Cog):
    CATEGORY_IDS = {
        1054090810800472154,
        985976523607650415,
        1194627560294842399,
        1194629375207952505,
        1165684137735241840,
        1194632735453630565,
    }
    EXCLUDED_CHANNEL_IDS = {
        1194722939342426306,
        1194723009563476089,
        1181566295540518992,
    }
    PUBLISH_CHANNEL_IDS = {
        1115726593457926294,
        1003589695910973480,
        1110173625778196581,
        1054091901852209252,
        1054091728816181328,
        1054091953433747539,
        1082393894190321835,
        1179067756918882386,
    }

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if await AutoMod(self.bot, message).process_automod():
            return

        if message.guild is None or message.guild.id != vhf:
            return

        category_id = getattr(message.channel, "category_id", None)
        parent = getattr(message.channel, "parent", None)
        if category_id is None and parent is not None:
            category_id = getattr(parent, "category_id", None)

        if category_id not in self.CATEGORY_IDS:
            return
        if message.channel.id in self.EXCLUDED_CHANNEL_IDS:
            return

        if message.attachments:
            try:
                await message.add_reaction(
                    PartialEmoji(name="mhxaLove", id=1174261737697050625)
                )
            except HTTPException:
                pass

            if message.channel.id in self.PUBLISH_CHANNEL_IDS:
                if (
                    isinstance(message.channel, TextChannel)
                    and message.channel.is_news()
                ):
                    try:
                        await message.publish()
                    except HTTPException:
                        pass


async def setup(bot: Bot):
    await bot.add_cog(OnMessageCog(bot))
