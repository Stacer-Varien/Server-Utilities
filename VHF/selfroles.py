from discord import (
    ButtonStyle,
    Color,
    Embed,
    Emoji,
    Message,
    Object,
    RawReactionActionEvent,
    ui,
)
from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from asyncio import sleep
from assets.buttons import EventRolesButtons


class SelfRolesCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    pride_button = ui.View().add_item(
        ui.Button(
            style=ButtonStyle.green,
            label="Pride Month",
            emoji="🌈",
            custom_id="pride",
        )
    )

    halloween_button = ui.View().add_item(
        ui.Button(
            style=ButtonStyle.green,
            label="Halloween",
            emoji="🎃",
        )
    )

    elf_button = ui.View().add_item(
        ui.Button(
            style=ButtonStyle.green,
            label="Elf Week",
            emoji="🧝",
            custom_id="elf",
        )
    )

    @tasks.loop(hours=1)
    async def selfroles(self):
        view=EventRolesButtons()
        vhf = await self.bot.fetch_guild(974028573893595146)
        eventroles_channel = await vhf.fetch_channel(1115725010649235608)
        pride = await eventroles_channel.fetch_message(1199715720146210846)
        halloween = await eventroles_channel.fetch_message(1199718222518296616)
        elf = await eventroles_channel.fetch_message(1199719535566143608)

        await pride.edit(view=view.pride)
        await sleep(5)
        await halloween.edit(view=view.halloween)
        await sleep(5)
        await elf.edit(view=view.elf)
        await sleep(5)



async def setup(bot: Bot):
    await bot.add_cog(SelfRolesCog(bot), guild=Object(974028573893595146))
