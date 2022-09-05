from nextcord import ui, ButtonStyle, Interaction


class AppButtons(ui.View):
    def __init__(self):
        super().__init__(timeout=1000)
        self.value = None

    @ui.button(label="Moderator", style=ButtonStyle.red)
    async def mod(self, button: ui.Button, ctx: Interaction):
        self.value = "mod"
        self.stop()

    @ui.button(label="Partnership Manager", style=ButtonStyle.green)
    async def pm(self, button: ui.Button, ctx: Interaction):
        self.value = "pm"
        self.stop()

    @ui.button(label="Security Officer", style=ButtonStyle.green)
    async def secure(self, button: ui.Button, ctx: Interaction):
        self.value = "secure"
        self.stop()

    @ui.button(label="Human Resources", style=ButtonStyle.green)
    async def hr(self, button: ui.Button, ctx: Interaction):
        self.value = "hr"
        self.stop()


class StartApp(ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.value = None

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = True
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = False
        self.stop()
