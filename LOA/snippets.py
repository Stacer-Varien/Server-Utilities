from typing import List, Optional
from discord import Color, Message, SelectOption, app_commands as Serverutil, Embed, Interaction, ui
from discord.ext.commands import Bot, Cog


class SnippetMenu(ui.Select):
    def __init__(self, message:Message):
        self.message=message

        options = [
            SelectOption(
                lable="Ask", description="Ask the member if they need assistance"
            ),
            SelectOption(
                label="Affiliate",
                description="Send requirements and intructions of affiliation",
            ),
            SelectOption(
                label="Partner",
                description="Send requirements and intructions of partnership",
            ),
            SelectOption(
                label="Channel-4-Channel",
                description="Send requirements and intructions of doing a channel-4-channel",
            ),
            SelectOption(
                label="More Help",
                description="Ask the member if they need more assistance",
            ),
            SelectOption(label="Alert HR", description="Alert the HR Department"),
            SelectOption(
                label="Alert Mods", description="Alert the Moderation Department"
            ),
            SelectOption(label="Alert PM", description="Alert the PM Department"),
            SelectOption(label="Alert Management", description="Alert Management"),
            SelectOption(label="Alert Core Team", description="Alert Core Team"),
        ]

        super().__init__(
            placeholder="Select an option", min_values=1, max_values=1, options=options
        )

    async def callback(self, ctx: Interaction):
        global snip
        if self.values[0] == "Ask":
            snip = "Thank you for opening a ticket! **What may I help you with**?"
        if self.values[0] == "Affiliate":
            snip="""
Requirements:
- More than **100** members.
- **Consistently** have at least **10** daily joins
> **Exceptions**: If you are willing to place our link at the bottom of your affiliating list and you **consistently** have **5** daily joins until you meet our requirement.
- **Safe** for work.
- Have **ping on join** enabled.

Steps:
1. Create a **ticket** via https://ptb.discord.com/channels/704888699590279221/715752926685167658.
2. Send a **permanent** invite link and clearly state that you want to **affiliate**.
3. **Post** our invite link (`https://discord.gg/xbtEbXzUty`) in your affiliates channel with **ping on join.**
4. **Tell** us once you have posted our invite link.
"""
        if self.values[0] == "Partner":
            snip = """
Requirements:
- More than **100** members.
- **Safe** for work.

Steps:
1. Create a **ticket** via https://ptb.discord.com/channels/704888699590279221/715752926685167658.
2. Send your **advertisement** and clearly state that you want to **partner**.
3. **Post** our advertisement (#📖・our-ad) in your partnership channel.
4. Tell us once you have posted our advertisement.
"""
        if self.values[0] == "Channel-4-Channel":
            snip="""
Requirements:
- More than **1,000** members.
> Exceptions: If you are willing to enable ping on join, we can do it too. 
- **Safe** for work.

Steps:
1. Create a **ticket** via https://ptb.discord.com/channels/704888699590279221/715752926685167658.
2. Send your **advertisement**, clearly state that you want to do **channel for channel** and tell us what you want us to name your channel.
3. **Create** a channel called ":chart_with_upwards_trend:・ join4members".
4. **Post** our advertisement (#📖・our-ad) in the custom channel you created.
5. **Tell** us once you have posted created the custom channel and posted our advertisement.

Options
- Ping on join
> If you have a consistent **50** daily joins, we can both do ping on join.

We will create the custom channel in the `Spotlight` category.
"""
        if self.values[0] == "More Help":
            snip = "Is there anything else I can assist you with?"

        await self.message.reply(embed=Embed(description=snip, color=Color.random()), mention_author=True)

class SnippetSelet(ui.View):
    def __init__(self, message:Message):
        super().__init__()

        self.add_item(SnippetMenu(message))


class SnippetsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.snip_general_context = Serverutil.ContextMenu(
            name="Snippets", callback=self.snip_general_callback
        )
        self.bot.tree.add_command(self.snip_general_context)


    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.snip_general_context.name, type=self.snip_general_context.type
        )


    async def snip_general_callback(self, ctx: Interaction, message: Message) -> None:
        view = SnippetSelet()
        await ctx.response.defer(ephemeral=True)
        await ctx.followup
        await ctx.followup.send(view=view)       

    @Serverutil.command()
    @Serverutil.checks.has_any_role(
        919410986249756673, 849778145087062046, 1160575171732721715
    )
    async def snippet(self, ctx: Interaction):
        ...


async def setup(bot: Bot):
    await bot.add_cog(SnippetsCog(bot))
