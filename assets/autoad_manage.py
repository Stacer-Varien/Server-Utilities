from discord import ui, ButtonStyle, Interaction


class AutoadManage(ui.View):

    def __init__(self):
        super().__init__(timeout=600)
        self.value = None

    @ui.button(label="Start", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = "start"

    @ui.button(label="Stop", style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = "stop"

    @ui.button(label="Cancel", style=ButtonStyle.danger)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = "cancel"

    @ui.button(label="Change Ad", style=ButtonStyle.blurple)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = "change_ad"
        self.stop()