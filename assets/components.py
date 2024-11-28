from io import BytesIO
from discord.ext.commands import Bot
from discord import User, ui, ButtonStyle, Interaction, File, SelectOption


class Confirmation(ui.View):
    def __init__(self, author:User=None):
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

    async def ctx_check(self, ctx: Interaction) -> bool:
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


