from discord import SelectOption, app_commands as Serverutil, Embed, Interaction, ui
from discord.ext.commands import Bot, Cog

class SnippetMenu(ui.Select):
    options = [SelectOption(lable="Ask"), SelectOption(label="")]

class SnippetsCog(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
    
    @Serverutil.command()
    @Serverutil.checks.has_any_role(919410986249756673, 849778145087062046, 1160575171732721715)
    async def snippet(self, ctx:Interaction)

async def setup(bot:Bot):
    await bot.add_cog(SnippetsCog(bot))