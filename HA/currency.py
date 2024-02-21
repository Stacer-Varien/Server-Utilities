from json import loads
from random import choice, randint
from typing import Literal, Optional
from discord import (
    ButtonStyle,
    Color,
    Embed,
    File,
    Member,
    TextChannel,
    app_commands as Serverutils,
    Interaction,
    ui,
)
from datetime import datetime, timedelta
from discord.ext.commands import Cog, Bot, GroupCog
from assets.functions import Currency
from assets.receipt_generator.generator import generator
from assets.components import AutoAdChannelSelect


class currencyCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).get_balance

        balance = Embed(
            description=f"{'You' if (member == ctx.user) else member} have {bal} <:HAZEcoin:1209238914041118721>",
            color=Color.blue(),
        )

        await ctx.followup.send(embed=balance)

    @Serverutils.command(description="Claim your daily")
    async def daily(self, ctx: Interaction):

        await ctx.response.defer()
        bank = Currency(ctx.user)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())

        if bank.check_daily:
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

            daily.add_field(
                name=rewards_text,
                value=rewards_value,
            )

            daily.add_field(
                name="Balance",
                value=f"{bank.get_balance} <:HAZEcoin:1209238914041118721>",
            )
            daily.add_field(name="Next Daily:", value=f"<t:{tomorrow}:f>")

            await ctx.followup.send(embed=daily)
        else:
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is <t:{bank.check_daily}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    @Serverutils.command(description="Check how much HAZE Coins you have")
    @Serverutils.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def balance(self, ctx: Interaction, member: Optional[Member] = None):

        member = ctx.user if (member == None) else member
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
    async def buy(
        self,
        ctx: Interaction,
        tier: Literal["Tier 1", "Tier 2", "Tier 3", "Tier 4"],
        custom_webhook: Optional[bool] = False,
        days: Optional[Serverutils.Range[int, 1, 40]] = 7,
        channels: Optional[bool] = False,
    ):
        await ctx.response.defer()
        if channels == True:
            view = AutoAdChannelSelect(self.bot, tier, days,custom_webhook)
            embed = Embed(color=Color.random())
            embed.description = "Which channels do you want your ad to be posted in?"
            await ctx.followup.send(embed=embed, view=view)
            return
        receipt=generator().generate_receipt(
            ctx.user, "Autoad", tier, custom_webhook, "♾🔄-unlimited🔄♾",days
        )
        file = File(fp=receipt, filename=f"autoad_receipt.png")
