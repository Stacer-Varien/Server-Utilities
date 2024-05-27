from io import BytesIO
from discord.ext.commands import Bot
from discord import ui, ButtonStyle, Interaction, File, SelectOption

from assets.receipt_generator.generator import ReceiptGenerator


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


class AutoadChannelMenu(ui.Select):
    def __init__(
        self, bot: Bot, tier: str, days: int, custom_webhook: bool = False
    ) -> None:
        self.bot = bot
        self.tier = tier
        self.days = days
        self.custom_webhook = custom_webhook
        super().__init__(
            placeholder="Select the channels",
            min_values=1,
            max_values=6,
            options=[
                SelectOption(
                    label=bot.get_channel(j).name, value=bot.get_channel(j).name
                )
                for j in [
                    1241276362359050330,
                    1241276387348844554,
                    1239500814301532233,
                    1239501940971274291,
                    1239502571727487017,
                    1239503912285765682,
                    1239504433465790524,
                    1239504190926094346,
                    1239502832533635143,
                    1239502264872472586,
                    1239503470453723186,
                    1239502181418143744,
                    1240194116810178650,
                ]
            ],
        )

    async def callback(self, ctx: Interaction):
        modal = AdInsertModal(
            self.bot, "Autoad", self.tier, self.custom_webhook, self.values, self.days
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

        self.ad = ui.TextInput(
            label="Insert Ad",
            placeholder="Place your ad here. Make sure to use permanent invites",
            required=True,
            min_length=40,
            max_length=2000,
        )
        self.add_item(self.ad)

    async def on_submit(self, ctx: Interaction) -> None:
        advert = File(BytesIO(self.ad.value.encode("utf-8")), filename="advert.txt")
        receipt_generator = ReceiptGenerator()

        if self.type == "Autoad":
            await ctx.response.edit_message(
                content="Please wait for your receipt to be generated",
                embed=None,
                view=None,
            )
            receipt = await receipt_generator.generate_receipt(
                ctx.user,
                self.type,
                self.tier,
                self.custom_webhook,
                self.channels,
                self.days,
            )
        elif self.type == "Giveaway":
            await ctx.response.edit_message(
                content="Please wait for your receipt to be generated"
            )
            receipt = await receipt_generator.generate_receipt(
                ctx.user,
                self.type,
                self.tier,
                self.days,
                winners=self.winners,
                custom_prize=self.prizes,
                use_alt_link=self.use_of_alt_link,
                ping=self.use_of_pings,
            )

        if receipt is None:
            return

        receiptchannel = await ctx.guild.fetch_channel(1211673783774224404)
        await receiptchannel.send(files=[receipt, advert])
        await ctx.edit_original_response(
            content="Thank you for purchasing. A copy of your receipt has been given to you. Please wait up to 36 hours for your product to be delivered",
            attachments=[receipt],
        )
