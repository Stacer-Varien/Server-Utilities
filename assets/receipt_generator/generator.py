from io import BytesIO
from typing import Optional, List
from discord import File, Interaction
from datetime import datetime
from assets.functions import Currency


class ReceiptGenerator:
    def __init__(self) -> None:
        pass

    async def generate_receipt(
        self,
        ctx: Interaction,
        type: str,
        tier: Optional[str] = None,
        days: Optional[int] = None,
        winners: Optional[int] = 1,
        custom_prize: Optional[str] = None,
        use_alt_link: Optional[bool] = False,
        ping: Optional[str] = "Giveaway Ping",
        servers: Optional[str] = None,
        channels: Optional[List[str]] = None,
    ) -> Optional[File]:
        bank_instance = Currency(ctx.user)
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        main_template = f"""
Orleans Advertising Orleans Coins Receipt
=====
Customer: {ctx.user}
Customer ID: {ctx.user.id}
Date of Purchase: {current_time}
"""

        cost, products_template = 0, ""

        if type == "Giveaway":
            tier_costs = {"Tier 1": 1000, "Tier 2": 1250, "Tier 3": 1500}
            tier_prizes = {
                "Tier 1": "Premium Role for 10 days",
                "Tier 2": "Shoutout with Shoutout Ping",
                "Tier 3": "Autoad per 5 hours in ⁠♾🔄-unlimited🔄♾ for 7 days",
            }
            tier_days = {"Tier 1": 3, "Tier 2": 3, "Tier 3": 4}
            cost = tier_costs.get(tier, 0)
            prize = custom_prize or tier_prizes.get(tier, "")
            cost += len(custom_prize.split(",")) * 50 if custom_prize else 0
            days = days if days is not None else tier_days.get(tier, 0)
            cost += (days - tier_days.get(tier, 0)) * 50
            can_use_alternative_link = "Yes" if use_alt_link else "No"
            cost += 50 if use_alt_link else 0
            ping_costs = {"Everyone": 200, "Here": 150}
            pings = ping if ping in ping_costs else None
            cost += ping_costs.get(ping, 0)

            products_template = f"""
Product description:
• {winners} winner(s)
• Prize: {prize}
• Ping: {pings}
• Duration: {days} days
• Required to join your server: Yes
• Can use social links as alternative: {can_use_alternative_link}

TOTAL COST = {cost} Orleans Coins
=====
Thank you for buying from Orleans Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 Orleans Advertising
"""

        elif type == "Premium":
            cost = 1500
            products_template = """
Product description: 
• Premium Role for life

TOTAL COST = 1500 Orleans Coins
=====
Thank you for buying from Orleans Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 Orleans Advertising
"""

        elif type == "Special Servers":
            cost = 1000
            if servers:
                server_count = len(servers.split(","))
                cost += (server_count - 1) * 50
            days = days if days is not None else 30
            cost += (days - 30) * 50

            products_template = f"""
Product description:
• Server's invite will be posted in 👋👤joins-and-leaves👤👋 when someone joins
• Server(s): {servers}
• Days: {days} days

TOTAL COST = {cost} Orleans Coins
=====
Thank you for buying from Orleans Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 Orleans Advertising
"""

        elif type == "Autoad":
            tier_costs = {"Tier 1": 1000, "Tier 2": 1500, "Tier 3": 2000}
            autoad_timers = {
                "Tier 1": "12 hours",
                "Tier 2": "8 hours",
                "Tier 3": "4 hours",
            }
            cost = tier_costs.get(tier, 0)
            autoad_timer = autoad_timers.get(tier, "")
            chnls = ",".join(channels) if channels else ""
            cost += (
                0
                if len(channels) == 1 and channels[0] == "⁠♾🔄-unlimited🔄♾"
                else len(channels) * 200
            )
            days = days if days is not None else 7
            cost += (days - 7) * 200

            products_template = f"""
Product description:
• Autoposting ad: Every {autoad_timer}
• Duration: {days} days
• Channels: {chnls}

TOTAL COST = {cost} Orleans Coins
=====
Thank you for buying from Orleans Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 Orleans Advertising
"""

        elif type == "YouTube Notifier":
            cost = 1000
            chnls = ",".join(channels) if channels else ""
            cost += (len(channels) - 1) * 50
            days = days if days is not None else 30
            cost += (days - 30) * 50

            products_template = f"""
Product description:
• YouTube videos will be posted in 📺youtube📺
• Channels: {chnls}
• Days: {days} days

TOTAL COST = {cost} Orleans Coins
=====
Thank you for buying from Orleans Advertising with your coins. Please wait up to 24 to 36 hours to have your service delivered.

        © 2024 Orleans Advertising
"""

        if bank_instance.balance < cost:
            await ctx.edit_original_response(
                "Your balance is too low. Please try again when you have sufficient funds."
            )
            return None

        await bank_instance.remove_credits(cost)
        complete_receipt = main_template + products_template
        file = BytesIO(complete_receipt.encode("utf-8"))
        return File(file, filename=f"{ctx.user}'s_{type}_receipt.txt")
