from config import loa
from discord import (
    AllowedMentions,
    CategoryChannel,
    Color,
    Message,
    Object,
    SelectOption,
    app_commands as Serverutil,
    Embed,
    Interaction,
    ui,
)
from discord.ext.commands import Bot, Cog


class SnippetMenu(ui.Select):
    def __init__(self, message: Message):
        self.message = message

        options = [
            SelectOption(
                label="Ask", description="Ask the member if they need assistance"
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
        ]

        super().__init__(
            placeholder="Select an option", min_values=1, max_values=1, options=options
        )

    async def callback(self, ctx: Interaction):
        global snip
        if self.values[0] == "Ask":
            snip = "Thank you for opening a ticket! **What may I help you with**?"
        elif self.values[0] == "Affiliate":
            snip = """
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
        elif self.values[0] == "Partner":
            snip = """
Requirements:
- More than **100** members.
- **Safe** for work.

Steps:
1. Create a **ticket** via https://ptb.discord.com/channels/704888699590279221/715752926685167658.
2. Send your **advertisement** and clearly state that you want to **partner**.
3. **Post** our advertisement (https://discord.com/channels/704888699590279221/1165211510537203722) in your partnership channel.
4. Tell us once you have posted our advertisement.
"""
        elif self.values[0] == "Channel-4-Channel":
            snip = """
Requirements:
- More than **1,000** members.
- Exceptions: If you are willing to enable ping on join, we can do it too. 
- **Safe** for work.

Steps:
1. Create a **ticket** via https://ptb.discord.com/channels/704888699590279221/715752926685167658.
2. Send your **advertisement**, clearly state that you want to do **channel for channel** and tell us what you want us to name your channel.
3. **Create** a channel called ":chart_with_upwards_trend:・ join4members".
4. **Post** our advertisement (https://discord.com/channels/704888699590279221/1165211510537203722) in the custom channel you created.
5. **Tell** us once you have posted created the custom channel and posted our advertisement.

Options
- Ping on join
> If you have a consistent **50** daily joins, we can both do ping on join.

We will create the custom channel in the https://discord.com/channels/704888699590279221/850925345879621633 category.
"""
        elif self.values[0] == "More Help":
            snip = "Is there anything else I can assist you with?"

        await ctx.response.edit_message(content="Response sent", view=None)
        await self.message.reply(
            embed=Embed(description=snip, color=Color.random()), mention_author=True
        )


class SnippetPingMenu(ui.Select):
    def __init__(self, message: Message):
        self.message = message

        options = [
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
        if self.values[0] == "Alert HR":
            snip = "Please wait while we transfer this ticket to the <@&1160570116350672896>"
        elif self.values[0] == "Alert Mods":
            snip = "Please wait while we transfer this ticket to the <@&1154076194837373021>"
        elif self.values[0] == "Alert PM":
            snip = "Please wait while we transfer this ticket to the <@&709677053926178859>"
        elif self.values[0] == "Alert Management":
            snip = "Please wait while we transfer this ticket to the <@&849778145087062046>"
        elif self.values[0] == "Alert Core Team":
            snip = "Please wait while we transfer this ticket to the <@&919410986249756673>"

        await ctx.response.edit_message(content="Response sent", view=None)
        await self.message.reply(
            snip,
            allowed_mentions=AllowedMentions(everyone=False, roles=True),
            mention_author=True,
        )


class SnippetSelet(ui.View):
    def __init__(self, message: Message):
        self.message = message
        super().__init__()

        self.add_item(SnippetMenu(self.message))


class SnippetPingSelet(ui.View):
    def __init__(self, message: Message):
        self.message = message
        super().__init__()

        self.add_item(SnippetPingMenu(self.message))


class SnippetsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.snip_general_context = Serverutil.ContextMenu(
            name="Snippets", callback=self.snip_general_callback
        )
        self.bot.tree.add_command(self.snip_general_context)
        self.snip_ping_context = Serverutil.ContextMenu(
            name="Snippets Ping", callback=self.snip_ping_callback
        )
        self.bot.tree.add_command(self.snip_ping_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.snip_general_context.name, type=self.snip_general_context.type
        )
        self.bot.tree.remove_command(
            self.snip_ping_context.name, type=self.snip_general_context.type
        )

    @Serverutil.guilds(loa)
    @Serverutil.checks.has_any_role(
        919410986249756673, 849778145087062046, 1160575171732721715
    )
    async def snip_general_callback(self, ctx: Interaction, message: Message) -> None:
        await ctx.response.defer(ephemeral=True)
        category: CategoryChannel = await ctx.guild.fetch_channel(1154685546136866878)
        if ctx.channel.id in [i.id for i in category.text_channels]:
            view = SnippetSelet(message)
            await ctx.followup.send(view=view)
            return

        await ctx.followup.send(
            "Please use these commands in the https://discord.com/channels/704888699590279221/1154685546136866878 channels"
        )

    @Serverutil.guilds(loa)
    @Serverutil.checks.has_any_role(
        919410986249756673, 849778145087062046, 1160575171732721715
    )
    @Serverutil.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def snip_ping_callback(self, ctx: Interaction, message: Message) -> None:
        await ctx.response.defer(ephemeral=True)
        category: CategoryChannel = await ctx.guild.fetch_channel(1154685546136866878)
        if ctx.channel.id in [i.id for i in category.text_channels]:
            view = SnippetSelet(message)
            await ctx.followup.send(view=view)
            return

        await ctx.followup.send(
            "Please use these commands in the https://discord.com/channels/704888699590279221/1154685546136866878 channels"
        )

async def setup(bot: Bot):
    await bot.add_cog(SnippetsCog(bot), guild=Object(loa))
