from discord import User, ui, ButtonStyle, Interaction


class Confirmation(ui.View):
    def __init__(self, author: User | None = None, timeout: int = 600):
        super().__init__(timeout=timeout)
        self.value = None
        self.author = author

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, ctx: Interaction, button: ui.Button):
        if not ctx.response.is_done():
            await ctx.response.defer()
        self.value = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        if not ctx.response.is_done():
            await ctx.response.defer()
        self.value = False
        self.stop()

    async def interaction_check(self, ctx: Interaction) -> bool:
        if self.author is None:
            return True
        return ctx.user.id == self.author.id


class YesNoButtons(ui.View):
    def __init__(self, author: User | None = None, timeout: int = 600):
        super().__init__(timeout=timeout)
        self.value = None
        self.author = author

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, ctx: Interaction, button: ui.Button):
        if not ctx.response.is_done():
            await ctx.response.defer()
        self.value = True
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, ctx: Interaction, button: ui.Button):
        if not ctx.response.is_done():
            await ctx.response.defer()
        self.value = False
        self.stop()

    async def interaction_check(self, ctx: Interaction) -> bool:
        if self.author is None:
            return True
        return ctx.user.id == self.author.id
