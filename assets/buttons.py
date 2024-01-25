from typing import Optional

from discord import User, ui, ButtonStyle
from discord.interactions import Interaction


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


class EventRolesButtons(ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.value = None

    @ui.button(
        style=ButtonStyle.green,
        label="Pride Month",
        emoji="🌈",
    )
    async def pride(self, button: ui.Button, ctx: Interaction):
        button.disabled = True
        role = ctx.guild.get_role(1115726474318729257)

        if role in ctx.user.roles:
            return
        await ctx.user.add_roles(role, reason="Pride Month Event")

    @ui.button(
        style=ButtonStyle.green,
        label="Halloween",
        emoji="🎃",
    )
    async def halloween(self, button: ui.Button, ctx: Interaction):
        button.disabled = True
        role = ctx.guild.get_role(1153989722327228486)

        if role in ctx.user.roles:
            return
        await ctx.user.add_roles(role, reason="Spooktober Event")

    @ui.button(
        style=ButtonStyle.green,
        label="Elf Week",
        emoji="🧝",
    )
    async def elf(self, button: ui.Button, ctx: Interaction):
        button.disabled = True
        role = ctx.guild.get_role(1170038274723684466)

        if role in ctx.user.roles:
            return
        await ctx.user.add_roles(role, reason="Elf Week Event")
