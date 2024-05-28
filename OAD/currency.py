from datetime import datetime, timedelta
from typing import Optional, Literal

from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Object,
    app_commands as Serverutils,
)
from discord.ext.commands import Cog, Bot, GroupCog

from assets.receipt_generator.generator import ReceiptGenerator
from config import hazead
from assets.functions import Currency
from assets.components import AdInsertModal, AutoAdChannelSelect


class CurrencyCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).balance

        balance = Embed(
            description=f"{'You' if member == ctx.user else member} have {bal} <:HAZEcoin:1209238914041118721>",
            color=Color.blue(),
        )

        await ctx.followup.send(embed=balance)

    @Serverutils.command(description="Claim your daily reward")
    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        bank = Currency(ctx.user)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())

        if bank.check_daily():
            await bank.give_daily()

            daily = Embed(
                title="Daily",
                description=f"**{ctx.user}**, you claimed your daily reward.",
                color=Color.random(),
            )

            is_weekend = datetime.today().weekday() >= 5
            rewards_text = "Rewards (weekend):" if is_weekend else "Rewards:"
            rewards_value = (
                "You received 200 <:HAZEcoin:1209238914041118721>"
                if is_weekend
                else "You received 100 <:HAZEcoin:1209238914041118721>"
            )

            daily.add_field(name=rewards_text, value=rewards_value)
            daily.add_field(
                name="Balance",
                value=f"{bank.balance} <:HAZEcoin:1209238914041118721>",
            )
            daily.add_field(name="Next Daily:", value=f"<t:{tomorrow}:f>")

            await ctx.followup.send(embed=daily)
        else:
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is <t:{bank.check_daily()}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    @Serverutils.command(description="Check your HAZE Coins balance")
    @Serverutils.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def balance(self, ctx: Interaction, member: Optional[Member] = None):
        member = ctx.user if member is None else member
        await self.get_balance(ctx, member)

    @balance.error
    async def balance_error(
        self, ctx: Interaction, error: Serverutils.errors.AppCommandError
    ):
        if isinstance(error, Serverutils.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class ShopCog(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Serverutils.command(
        name="buy-autoad", description="Buy an autoad plan with HAZE Coins"
    )
    @Serverutils.describe(
        custom_webhook="Should your ad be posted by a webhook?", days="How many days?"
    )
    async def buy_autoad(
        self,
        ctx: Interaction,
        tier: Literal["Tier 1", "Tier 2", "Tier 3", "Tier 4"],
        custom_webhook: Optional[bool] = False,
        days: Optional[Serverutils.Range[int, 7, 40]] = 7,
        channels: Optional[bool] = False,
    ):
        if channels:
            view = AutoAdChannelSelect(self.bot, tier, days, custom_webhook)
            embed = Embed(
                color=Color.random(),
                description="Which channels do you want your ad to be posted in?",
            )
            await ctx.followup.send(embed=embed, view=view)
            return
        modal = AdInsertModal(
            self.bot,
            type="Autoad",
            product=tier,
            custom_webhook=custom_webhook,
            channels=channels,
            days=days,
        )
        await ctx.response.send_modal(modal)

    @Serverutils.command(
        name="buy-giveaway", description="Buy a giveaway plan with HAZE Coins"
    )
    @Serverutils.describe(
        days="How many days?",
        winners="How many winners",
        prizes="Add your own prizes if you want. Split each prize after ','",
        use_of_alt_link="Should an alt link be used (such as YT channels, Twitch channels, etc)",
    )
    async def buy_giveaway(
        self,
        ctx: Interaction,
        tier: Literal["Tier 1", "Tier 2", "Tier 3"],
        days: Optional[Serverutils.Range[int, 3, 10]] = 3,
        winners: Optional[Serverutils.Range[int, 1, 5]] = 1,
        prizes: Optional[str] = None,
        use_of_pings: Optional[Literal["Everyone", "Here"]] = "Giveaway Ping",
        use_of_alt_link: Optional[bool] = False,
    ):
        modal = AdInsertModal(
            self.bot,
            type="Giveaway",
            product=tier,
            winners=winners,
            prizes=prizes,
            use_of_pings=use_of_pings,
            use_of_alt_link=use_of_alt_link,
            days=days,
        )
        await ctx.response.send_modal(modal)

    @Serverutils.command(
        name="buy-premium", description="Buy a permanent Premium role with HAZE Coins"
    )
    async def buy_premium(self, ctx: Interaction):
        await ctx.response.defer()
        await ctx.followup.send("Please wait for your receipt to be generated")
        receipt = await ReceiptGenerator().generate_receipt(
            ctx, ctx.user, "Premium for life"
        )
        if receipt is None:
            return
        await ctx.edit_original_response(
            content="Thank you for purchasing. The Premium Role has been given immediately to you",
            attachments=[receipt],
        )
        await ctx.user.add_roles(949733980951945306, reason="Bought Premium for life")
        receipt_channel = await ctx.guild.fetch_channel(1211673783774224404)
        await receipt_channel.send(file=receipt)

    @Serverutils.command(
        name="buy-special-servers",
        description="Buy a special servers plan with HAZE Coins",
    )
    @Serverutils.describe(
        servers="Add some invites. Split each one with ','. Only the first 3 will be picked"
    )
    async def buy_special_servers(
        self,
        ctx: Interaction,
        servers: str,
        days: Optional[Serverutils.Range[int, 30, 60]] = 30,
    ):
        await ctx.response.defer()
        await ctx.followup.send("Please wait for your receipt to be generated")
        receipt = await ReceiptGenerator().generate_receipt(
            ctx.user, "Special Servers", days=days, servers=servers
        )
        if receipt is None:
            return
        await ctx.edit_original_response(
            content="Thank you for purchasing. A copy of your receipt has been given to you. Please wait up to 36 hours for your product to be delivered",
            attachments=[receipt],
        )
        receipt_channel = await ctx.guild.fetch_channel(1211673783774224404)
        await receipt_channel.send(file=receipt)

    @Serverutils.command(
        name="buy-youtube-notifier",
        description="Buy a YouTube Notifier plan with HAZE Coins",
    )
    @Serverutils.describe(
        channels="Add some channels. Split each one with ','. Only the first 3 will be picked"
    )
    async def buy_youtube_notifier(
        self,
        ctx: Interaction,
        channels: str,
        days: Optional[Serverutils.Range[int, 30, 60]] = 30,
    ):
        await ctx.response.defer()
        await ctx.followup.send("Please wait for your receipt to be generated")
        receipt = await ReceiptGenerator().generate_receipt(
            ctx.user, "YouTube Notifier", days=days, channels=channels
        )
        if receipt is None:
            return
        await ctx.edit_original_response(
            content="Thank you for purchasing. A copy of your receipt has been given to you. Please wait up to 36 hours for your product to be delivered",
            attachments=[receipt],
        )
        receipt_channel = await ctx.guild.fetch_channel(1211673783774224404)
        await receipt_channel.send(file=receipt)


async def setup(bot: Bot):
    await bot.add_cog(CurrencyCog(bot), guild=Object(hazead))
    await bot.add_cog(ShopCog(bot), guild=Object(hazead))
