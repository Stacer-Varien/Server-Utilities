from io import BytesIO
from discord.ext.commands import Bot
from discord import ui, ButtonStyle, Interaction, File, SelectOption

from assets.receipt_generator.generator import ReceiptGenerator, generator


class Confirmation(ui.View):
    def __init__(self, author=None):
        super().__init__(timeout=600)
        self.value = None
        self.author = author

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button, ctx):
        self.value = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, button, ctx):
        self.value = False
        self.stop()

    async def interaction_check(self, ctx):
        return ctx.user.id == self.author.id


class YesNoButtons(ui.View):
    def __init__(self, timeout: int):
        super().__init__(timeout=timeout)
        self.value = None

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button, ctx):
        self.value = True
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button, ctx):
        self.value = False
        self.stop()


class AdModal(ui.Modal, title="Ad Modal"):
    def __init__(self) -> None:
        super().__init__()
        self.advalue = ui.TextInput(
            label="Ad",
            placeholder="Insert your ad here. Make sure theres a permanent invite and no custom emojis",
            required=True,
            min_length=1,
            max_length=2000,
        )

    async def on_submit(self, ctx: Interaction) -> None:
        file = File(
            BytesIO(self.advalue.value.encode("utf-8")), filename=f"{ctx.user}'s_ad.txt"
        )


class AutoadChannelMenu(ui.Select):
    def __init__(
        self, bot: Bot, tier: str, days: int, custom_webhook: bool = False
    ) -> None:
        self.bot=bot
        self.tier=tier
        self.days=days
        self.custom_webhook=custom_webhook
        super().__init__(
            placeholder="Select the channels",
            min_values=1,
            max_values=6,
            options=[
                SelectOption(
                    label=bot.get_channel(j).name, value=bot.get_channel(j).name
                )
                for j in [
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
            ],
        )

    async def callback(self, ctx: Interaction):
        channels = self.values
        modal = AdInsertModal(
            self.bot, "Autoad", self.tier, self.custom_webhook, channels, self.days
        )
        await ctx.response.send_modal(modal)


class AutoAdChannelSelect(ui.View):
    def __init__(self, bot: Bot, tier: str, days: int, custom_webhook: bool = False):
        super().__init__(timeout=180)
        self.add_item(AutoadChannelMenu(bot, tier, days, custom_webhook))


class AdInsertModal(ui.Modal, title="Ad Insert Modal"):
    def __init__(
        self,
        bot: Bot,
        type: str,
        tier: str,
        custom_webhook: bool = False,
        channels: list[str] = None,
        days: int = 7,
        winners: int = 1,
        prizes: list[str] = None,
        use_of_pings: str = None,
        use_of_alt_link: bool = False,
    ) -> None:
        super().__init__()
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

    ad = ui.TextInput(
        label="Insert Ad",
        placeholder="Place your ad here. Make sure to use permanent invites",
        required=True,
        min_length=40,
        max_length=2000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        advert = File(BytesIO(self.ad.value.encode("utf-8")), filename="advert.txt")
        if self.type == "Autoad":
            await ctx.response.edit_message(
                content="Please wait for your reciept to be generated",
                embed=None,
                view=None,
            )
            receipt = await ReceiptGenerator().generate_receipt(
                ctx.user,
                self.type,
                self.tier,
                self.custom_webhook,
                self.channels,
                self.days,
            )
            receipt = File(fp=receipt, filename=f"autoad_receipt.png")
            receiptchannel = await ctx.guild.fetch_channel(1211673783774224404)
            await receiptchannel.send(files=[receipt, advert])
            await ctx.edit_original_response(
                content="Thank you for purchasing. A copy of your receipt has been given to you. Please wait up to 36 hours for your product to be delivered",
                attachments=[receipt],
            )
