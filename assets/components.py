from io import BytesIO
from typing import Optional
from discord.ext.commands import Bot
from discord import Color, Embed, File, SelectOption, User, ui, ButtonStyle, TextStyle
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


class AdModal(ui.Modal, title="Ad Modal"):
    def __init__(self) -> None:
        super().__init__()

    advalue = ui.TextInput(
        label="Ad",
        style=TextStyle.paragraph,
        placeholder="Insert your ad here. Make sure theres a permanent invite and no custom emojis",
        required=True,
        min_length=1,
        max_length=2000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        file = BytesIO(self.advalue.value.encode("utf-8"))
        file = File(file, filename=f"{ctx.user}'s_ad.txt")


class AutoadChannelMenu(ui.Select):
    def __init__(
        self, bot: Bot, tier: str, days: int, custom_webhook: bool = False
    ) -> None:
        self.bot=bot
        self.tier = tier
        self.custom_webhook = custom_webhook
        self.days = days
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

        options = [
            SelectOption(label=i.name, value=i.name)
            for i in [self.bot.get_channel(j) for j in channelids]
        ]
        super().__init__(
            placeholder="Select the channels",
            min_values=1,
            max_values=6,
            options=options,
        )

    async def callback(self, ctx: Interaction):
        channels = [i for i in self.values]
        modal = AdInsertModal(self.bot,
            "Autoad", self.tier, self.custom_webhook, channels, self.days
        )
        await ctx.response.send_modal()
        await ctx.response.edit_message(
            content="Please wait for your reciept to be generated",
            embed=None,
            view=None,
        )

        receipt = generator().generate_receipt(
            ctx.user, "Autoad", self.tier, self.custom_webhook, channels, self.days
        )
        file = File(fp=receipt, filename=f"autoad_receipt.png")
        await ctx.edit_original_response(content=None, attachments=[file])


class AutoAdChannelSelect(ui.View):
    def __init__(self, bot: Bot, tier: str, days: int, custom_webhook: bool = False):
        self.bot = bot
        self.tier = tier
        self.custom_webhook = custom_webhook
        self.days = days
        super().__init__(timeout=180)
        self.add_item(
            AutoadChannelMenu(self.bot, self.tier, self.days, self.custom_webhook)
        )


class AdInsertModal(ui.Modal, title="Ad Insert Modal"):

    def __init__(
        self,
        bot: Bot,
        type: str,
        tier: str,
        custom_webhook: Optional[bool] = False,
        channels: Optional[list[str]] = None,
        days: Optional[int] = 7,
        winners: Optional[int] = 1,
        prizes: Optional[list[str]] = None,
        use_of_pings: Optional[str] = None,
        use_of_alt_link: Optional[bool] = False,
    ) -> None:
        self.bot = bot
        self.type = type
        self.tier = tier
        self.custom_webhook = custom_webhook
        self.channels = channels
        self.days = days
        self.winners = winners
        self.prizes = prizes
        self.use_of_pings = use_of_pings
        self.use_of_alt_link = use_of_alt_link
        super().__init__()

    ad = ui.TextInput(
        label="Insert Ad",
        style=TextStyle.paragraph,
        placeholder="Place your ad here. Make sure to use permanent invites",
        required=True,
        min_length=40,
        max_length=2000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        advert = BytesIO(self.ad.value.encode("utf-8"))
        advert = File(advert, filename="advert.txt")
        if self.type == "Autoad":
            if self.channels == True:
                view = AutoAdChannelSelect(
                    self.bot, self.tier, self.days, self.custom_webhook
                )
                embed = Embed(color=Color.random())
                embed.description = (
                    "Which channels do you want your ad to be posted in?"
                )
                await ctx.response.edit_message(embed=embed, view=view)
                return
            await ctx.response.edit_message(
                content="Please wait for your receipt to be generated",
                embed=None,
                view=None,
            )
            receipt = await generator().generate_receipt(ctx,
                ctx.user,
                self.type,
                self.tier,
                self.custom_webhook,
                ["♾🔄-unlimited🔄♾"],
                self.days,
            )
            receipt = File(fp=receipt, filename=f"autoad_receipt.png")
            await ctx.edit_original_response(
                content="Thank you for purchasing. A copy of your receipt has been given to you. Please wait up to 36 hours for your product to be delivered",
                attachments=[receipt, advert],
            )
