from io import BytesIO
import os
from random import randint
from typing import Optional, List
from discord import File, Interaction, Member
from datetime import datetime
from assets.functions import Currency


class ReceiptGenerator:
    def __init__(self) -> None:
        pass

    async def generate_receipt(
        self,
        ctx: Interaction,
        type: str,
        tier: Optional[str]=None,
        days: Optional[int] = None,
        winners: Optional[int] = 1,
        custom_prize: Optional[str] = None,
        use_alt_link: Optional[bool] = False,
        ping: Optional[str] = "Giveaway Ping",
        servers: Optional[str] = None,
        channels: Optional[List[str]] = None,
    )->File | None:
        bank_instance = Currency(ctx.user)
        main_template = f"""
HAZE Advertising HAZE Coins Receipt
=====
Customer: {ctx.user}
Customer ID: {ctx.user.id}
Date of Purchase: {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
        if type == "Giveaway":
            if tier == "Tier 1":
                cost = 1000
                prize = (
                    custom_prize
                    if custom_prize is not None
                    else "Premium Role for 10 days"
                )
                cost += (
                    len(custom_prize.split(",")) * 50 if custom_prize is not None else 0
                )
                days = days if days is not None else 3
                cost += (days - 3) * 50
                can_use_alternative_link = "No" if not use_alt_link else "Yes"
                cost += 50 if use_alt_link else 0
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost += 200 if ping == "Everyone" else 150 if ping == "Here" else 0

            elif tier == "Tier 2":
                cost = 1250
                prize = (
                    custom_prize
                    if custom_prize is not None
                    else "Shoutout with Shoutout Ping"
                )
                cost += (
                    len(custom_prize.split(",")) * 50 if custom_prize is not None else 0
                )
                days = days if days is not None else 3
                cost += (days - 3) * 50
                can_use_alternative_link = "Yes"
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost += 200 if ping == "Everyone" else 150 if ping == "Here" else 0

            elif tier == "Tier 3":
                cost = 1500
                prize = (
                    custom_prize
                    if custom_prize is not None
                    else "Autoad per 5 hours in ⁠♾🔄-unlimited🔄♾ for 7 days"
                )
                cost += (
                    len(custom_prize.split(",")) * 50 if custom_prize is not None else 0
                )
                days = days if days is not None else 4
                cost += (days - 4) * 50
                can_use_alternative_link = "Yes"
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost += 200 if ping == "Everyone" else 150 if ping == "Here" else 0

            products_template = f"""
Product description:
• {winners} winner(s)
• Prize: {prize}
• Ping: {pings}
• Duration: {days} days
• Required to join your server: Yes
• Can use social links as alternative: {can_use_alternative_link}

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "Premium":
            cost = 1500
            products_template = """
Product description: 
• Premium Role for life

TOTAL COST = 1500 HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "Special Servers":
            cost = 1000
            if servers and len(servers.split()) > 1:
                cost += (len(servers.split()) - 1) * 50
            days = days if days is not None else 30
            cost += (days - 30) * 50

            products_template = f"""
Product description:
⁠• Server's invite will be posted in 👋👤joins-and-leaves👤👋 when someone joins
• Servers: {servers}
• Days: {days} days

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "Autoad":
            if tier == "Tier 1":
                cost = 1000
                autoad_timer = "12 hours"
                chnls = ",".join(channels) if len(channels) > 1 else channels[0]
                cost += (
                    0
                    if len(channels) == 1 and channels[0] == "⁠♾🔄-unlimited🔄♾"
                    else len(channels) * 200
                )
                days = days if days is not None else 7
                cost += (days - 7) * 200
            elif tier == "Tier 2":
                cost = 1500
                autoad_timer = "8 hours"
                chnls = ",".join(channels) if len(channels) > 1 else channels[0]
                cost += (
                    0
                    if len(channels) == 1 and channels[0] == channels[0]
                    else len(channels) * 200
                )
                days = days if days is not None else 7
                cost += (days - 7) * 200
            elif tier == "Tier 3":
                if len(channels) == 1:
                    cost = 2000
                    autoad_timer = "4 hours"
                    chnls = channels[0]
                elif len(channels) == 2:
                    cost = 2500
                    autoad_timer = "2 hours"
                    chnls = ",".join(channels)
                else:
                    cost = 2500
                    autoad_timer = "2 hours"
                    chnls = ",".join(channels)
                cost += 0 if len(channels) in [1, 2] else len(channels) * 200
                days = days if days is not None else 14
                cost += (days - 7) * 200

            products_template = f"""
Product description:
• Autoposting ad: Every {autoad_timer}
• Duration: {days} days
• Channels: {chnls}

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "YouTube Notifier":
            cost = 1000
            chnls = ",".join(channels) if len(channels) > 1 else channels[0]
            cost += (len(channels) - 1) * 50
            days = days if days is not None else 30
            cost += (days - 30) * 50

            products_template = f"""
Product description:
⁠• YouTube videos will be posted in 📺youtube📺
• Channels: {chnls}
• Days: {days} days

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""

        if bank_instance.get_balance() < cost:
            await ctx.edit_original_response(
                "Your balance is too low. Please try again when you have sufficient funds."
            )
            return

        await bank_instance.remove_credits(cost)
        complete_receipt = main_template + products_template
        file = BytesIO(complete_receipt.encode("utf-8"))
        file = File(file, filename=f"{ctx.user}'s_{type}_receipt.txt")
        return file
