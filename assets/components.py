from typing import Optional
from discord.ext.commands import Bot
from discord import SelectOption, User, ui, ButtonStyle, TextStyle
from discord.interactions import Interaction

from assets.receipt_generator.generator import generator


class Confirmation(ui.View):
    def __init__(self, author: Optional[User] = None):
        super().__init__(timeout=600)
        self.value = None
        self.author = author

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = False
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class YesNoButtons(ui.View):
    def __init__(self, timeout: int):
        super().__init__(timeout=timeout)
        self.value = None

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button: ui.Button, ctx: Interaction):
        self.value = True
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button: ui.Button, ctx: Interaction):
        self.value = False
        self.stop()


class AutoadChannelMenu(ui.Select):
    def __init__(self, bot:Bot, tier:str, days:int, custom_webhook:bool=False) -> None:
        self.tier=tier
        self.custom_webhook = custom_webhook
        self.days=days
        channelids = [
            925790261240561717,
            950356056456986624,
            925790261240561718,
            925790261240561719,
            925790261240561720,
            925790261240561722,
            1081955520094687272,
            1081955734146777138,
            952139192505344021,
            925790261240561723,
            925790261437669387,
            925790261437669390,
            951385958924828713,
            925790261437669392,
            925790260997283851,
            925790260997283853,
            925790260997283855,
            949733907392253952,
        ]

        options=[SelectOption(label=i.name, value=i.name) for i in [bot.get_channel(j) for j in channelids]]
        super().__init__(placeholder="Select the channels", min_values=1, max_values=6, options=options)

    async def callback(self, ctx: Interaction):
        channels = [i for i in self.values]
        generator().generate_receipt(
            ctx.user, "Autoad", self.tier, self.custom_webhook, channels, self.days
        )
        return 


class AutoAdChannelSelect(ui.View):
    def __init__(self, bot: Bot, tier: str, days: int, custom_webhook: bool = False):
        self.bot=bot
        self.tier = tier
        self.custom_webhook = custom_webhook
        self.days = days
        super().__init__(timeout=180)
        self.add_item(AutoadChannelMenu(self.bot))
