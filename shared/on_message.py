from datetime import timedelta
from discord import Message, Forbidden
from discord.ext.commands import Cog, Bot
from assets.buttons import Confirmation
from assets.functions import AutoMod


class AutomodCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if (
            message.guild.id == 974028573893595146
            and message.channel.id != 1173932523764600882
            and len(message.attachments) >= 1
        ):
            await message.add_reaction(":mhxaLove:1174261737697050625")
            return

        await AutoMod(self.bot, message).process_automod()
            


async def setup(bot: Bot):
    await bot.add_cog(AutomodCog(bot))
