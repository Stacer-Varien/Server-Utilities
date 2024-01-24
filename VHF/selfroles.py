from discord import ButtonStyle, Color, Embed, Emoji, PartialEmoji, ui, app_commands as ServerUtils
from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from asyncio import sleep


class SelfRolesCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.eventroles.start()

        self.buttons = {
            "pride": self.create_button("Pride Month", "🌈"),
            "halloween": self.create_button("Halloween", "🎃"),
            "elf": self.create_button("Elf Week", "🧝"),
        }

    def create_button(self, label:(str|None), emoji:(str | Emoji | PartialEmoji | None)):
        return ui.View().add_item(
            ui.Button(
                style=ButtonStyle.green,
                label=label,
                emoji=emoji,
                custom_id=label.lower()),
            )
        

    @tasks.loop(hours=1)
    async def eventroles(self):
        guild_id = 974028573893595146
        eventroles_channel_id = 1115725010649235608

        guild = await self.bot.fetch_guild(guild_id)
        eventroles_channel = await guild.fetch_channel(eventroles_channel_id)

        for button_id, message_id in [
            ("pride", 1199715720146210846),
            ("halloween", 1199718222518296616),
            ("elf", 1199719535566143608),
        ]:
            message = await eventroles_channel.fetch_message(message_id)
            await message.edit(view=self.buttons[button_id])
            await sleep(5)
    
    @ServerUtils.command("Di")


async def setup(bot: Bot):
    await bot.add_cog(SelfRolesCog(bot))
