from discord import Member, SelectOption, Interaction, TextChannel, ui
from shared.adwarn import WarnCog
from discord.ext.commands import Bot

class LOAdropdown(ui.Select):
    def __init__(self, bot:Bot, member:Member, channel:TextChannel):
        self.bot=bot
        self.member=member
        self.channel=channel

        options = [
            SelectOption(label="Ad has an invalid invite"),
            SelectOption(label="Back-to-Back advertising"),
            SelectOption(label="Ad contains a public ping or mention"),
            SelectOption(label="Ad is an invite reward server"),
            SelectOption(label="NSFW ad, imagery or description"),
            SelectOption(label="Advertising in wrong channel"),

        ]

        super().__init__(placeholder="Which warning will the member recieve", min_values=1, max_values=1, options=options)

    async def callback(self, ctx: Interaction):
        await WarnCog(self.bot).loa_warn(ctx, self.member, self.channel, self.values[0], None)


class LOAdropdownView(ui.View):
    def __init__(self, bot:Bot, member:Member, channel:TextChannel):
        self.bot=bot
        self.member=member
        self.channel=channel
        super().__init__()

        self.add_item(LOAdropdown(self.bot, self.member, self.channel))

class HAdropdown(ui.Select):
    def __init__(self, bot:Bot, member:Member, channel:TextChannel):
        self.bot=bot
        self.member=member
        self.channel=channel

        options = [
            SelectOption(label="Ad has an invalid invite"),
            SelectOption(label="Back-to-Back advertising"),
            SelectOption(label="Ad contains a public ping or mention"),
            SelectOption(label="Ad is an invite reward server"),
            SelectOption(label="NSFW ad, imagery or description"),
            SelectOption(label="Advertising in wrong channel"),
            SelectOption(label="Ad has short or no description"),
        ]

        super().__init__(placeholder="Which warning will the member recieve", min_values=1, max_values=1, options=options)

    async def callback(self, ctx: Interaction):
        await WarnCog(self.bot).ha_warn(ctx, self.member, self.channel, self.values[0], None)


class HAdropdownView(ui.View):
    def __init__(self, bot:Bot, member:Member, channel:TextChannel):
        self.bot=bot
        self.member=member
        self.channel=channel
        super().__init__()

        self.add_item(HAdropdown(self.bot, self.member, self.channel))