from io import BytesIO
import os
from random import randint
from typing import Optional, List
from discord import Interaction, Member
from datetime import datetime
from assets.functions import Currency


class ReceiptGenerator:
    def __init__(self) -> None:
        pass

    async def generate_receipt(
        self,
        ctx: Interaction,
        type: str,
        tier: str,
        days: Optional[int] = None,
        winners: Optional[int] = 1,
        custom_prize: Optional[str] = None,
        use_alt_link: Optional[bool] = False,
        ping: Optional[str] = "Giveaway Ping",
        servers:Optional[str]=None
    ) -> BytesIO:
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
                    custom_prize if custom_prize != None else "Premium Role for 10 days"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if (days != None) else 3
                cost = cost + ((days - 3) * 50)
                can_use_alternative_link = "No" if use_alt_link == False else "Yes"
                cost = cost + (50 if use_alt_link == True else 0)
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            elif tier == "Tier 2":
                cost = 1250
                prize = (
                    custom_prize
                    if custom_prize != None
                    else "Shoutout with Shoutout Ping"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if days != None else 3
                cost = cost + ((days - 3) * 50)
                can_use_alternative_link = "Yes" 
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            elif tier == "Tier 3":
                cost = 1500
                prize = (
                    custom_prize
                    if custom_prize != None
                    else " Autoad per 5 hours in ⁠♾🔄-unlimited🔄♾  for 7 days"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if days != None else 4
                cost = cost + ((days - 4) * 50)
                can_use_alternative_link = "Yes"
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            products_template = f"""
Product description:
• {winners} winner(s)
• Prize: {prize}
• Ping: {ping}
• Duration: {days} days
• Required to join your server: Yes
• Can use social links as alternative: {can_use_alternative_link}

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "Premium":
            cost=1500
            products_template = """
Product description: 
• Premium Role for life

TOTAL COST = 1500 HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""
        elif type == "SpecialServers":
            cost=1000
            if len(servers.split()) > 1:
                cost = cost + ((len(servers.split()) - 1) * 50)
            days= days if days != None else 30
            cost=cost +((days -30) * 50)

            products_template = f"""
Product description:
⁠• Server will be posted in 👋👤joins-and-leaves👤👋 when someone joins
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
                prize = (
                    custom_prize if custom_prize != None else "Premium Role for 10 days"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if (days != None) else 3
                cost = cost + ((days - 3) * 50)
                can_use_alternative_link = "No" if use_alt_link == False else "Yes"
                cost = cost + (50 if use_alt_link == True else 0)
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            elif tier == "Tier 2":
                cost = 1250
                prize = (
                    custom_prize
                    if custom_prize != None
                    else "Shoutout with Shoutout Ping"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if days != None else 3
                cost = cost + ((days - 3) * 50)
                can_use_alternative_link = "Yes" 
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            elif tier == "Tier 3":
                cost = 1500
                prize = (
                    custom_prize
                    if custom_prize != None
                    else " Autoad per 5 hours in ⁠♾🔄-unlimited🔄♾  for 7 days"
                )
                cost = cost + (
                    len(custom_prize.split(",") * 50) if custom_prize != None else 0
                )
                days = days if days != None else 4
                cost = cost + ((days - 4) * 50)
                can_use_alternative_link = "Yes"
                pings = (
                    "Everyone"
                    if ping == "Everyone"
                    else "Here" if ping == "Here" else None
                )
                cost = cost + (
                    200 if ping == "Everyone" else 150 if ping == "Here" else 0
                )

            products_template = f"""
Product description:
• {winners} winner(s)
• Prize: {prize}
• Ping: {ping}
• Duration: {days} days
• Required to join your server: Yes
• Can use social links as alternative: {can_use_alternative_link}

TOTAL COST = {cost} HAZE Coins
=====
Thank you for buying from HAZE Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 HAZE Advertising
"""