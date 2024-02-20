from json import loads
from random import choice, randint
from typing import Optional
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Member,
    app_commands as Serverutils,
    Interaction,
    ui,
)
from datetime import datetime, timedelta
from discord.ext.commands import Cog, Bot, GroupCog
from assets.functions import Currency


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
            rewards_value = "You received 200 <:HAZEcoin:1209238914041118721>" if is_weekend else "You received 100 <:HAZEcoin:1209238914041118721>"

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
    def __init__(self, bot:Bot) -> None:
        self.bot=bot
        super().__init__()
    
    @Serverutils.command(description="Buy a plan with HAZE Coins")
    async def buy(self, ctx:Interaction):
        ...
