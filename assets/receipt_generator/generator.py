from io import BytesIO
import os
from random import randint
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont
from discord import Interaction, Member
from datetime import datetime
from assets.functions import Currency


class ReceiptGenerator:
    def __init__(self) -> None:
        self.font = os.path.join(os.path.dirname(__file__), "absender1.ttf")

    async def generate_receipt(
        self, ctx: Interaction, member: Member, type: str, **kwargs
    ) -> BytesIO:
        bank_instance = Currency(member)
        receipt_template = os.path.join(os.path.dirname(__file__), "autoad.png")
        if type == "Giveaway":
            receipt_template = os.path.join(
                os.path.dirname(__file__), "assets", "receipt_generator", "giveaway.png"
            )
        elif type == "Premium":
            receipt_template = os.path.join(
                os.path.dirname(__file__), "assets", "receipt_generator", "premium.png"
            )
        elif type == "SpecialServers":
            receipt_template = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "receipt_generator",
                "specialservers.png",
            )

        rt_open = Image.open(receipt_template).convert("RGBA")
        draw = ImageDraw.Draw(rt_open)


        draw.text(
            (640, 540),
            text=member.name,
            fill=(0, 0, 0),
            font=ImageFont.truetype(self.font, 60),
        )
        draw.text(
            (640, 700),
            text=str(member.id),
            fill=(0, 0, 0),
            font=ImageFont.truetype(self.font, 60),
        )
        draw.text(
            (640, 820),
            text=datetime.now().strftime("%d/%m%Y"),
            fill=(0, 0, 0),
            font=ImageFont.truetype(self.font, 60),
        )

        if type == "Autoad":
            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )

            draw.text(
                (640, 950),
                text=kwargs.get("product"),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1110),
                text=str(kwargs.get("custom_webhook")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1170),
                text=str(kwargs.get("days")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1260),
                text="\n".join(kwargs.get("channels", [])),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )


            total_cost = self.calculate_autoad_cost(kwargs)
            if bank_instance.get_balance < total_cost:
                await ctx.edit_original_response(
                    "Your balance is too low. Please try again when you have sufficient funds"
                )
                return

            draw.text(
                (870, 2030),
                text=str(total_cost),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
        elif type == "Giveaway":

            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 950),
                text=kwargs.get("product"),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1120),
                text=str(kwargs.get("winners")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1210),
                text="Yes",
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1300),
                text=str(kwargs.get("use_of_alt_link")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1370),
                text=str(kwargs.get("use_of_pings")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1460),
                text="\n".join(kwargs.get("prizes", [])),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )


            total_cost = self.calculate_giveaway_cost(kwargs)
            draw.text(
                (1040, 1850),
                text=total_cost,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
        elif type == "Premium":
            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            total_cost = 1500
            if bank_instance.get_balance < total_cost:
                await ctx.edit_original_response(
                    "Your balance is too low. Please try again when you have sufficient funds"
                )
                return
            draw.text(
                (1080, 1000),
                text=str(total_cost),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
        elif type == "SpecialServers":
            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1000),
                text=str(kwargs.get("days")),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            draw.text(
                (640, 1130),
                text=str(len(kwargs.get("servers", "").split(","))),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )


            total_cost = self.calculate_special_servers_cost(kwargs)
            draw.text(
                (970, 1255),
                text=str(total_cost),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )

        final_bytes = BytesIO()
        rt_open.save(final_bytes, "png")
        final_bytes.seek(0)
        await bank_instance.remove_credits(int(total_cost))
        return final_bytes

    def calculate_autoad_cost(self, kwargs: dict) -> int:
        product = kwargs.get("product")
        days = kwargs.get("days")
        channels = kwargs.get("channels", [])
        custom_webhook = kwargs.get("custom_webhook")

        if product == "Tier 1":
            prdt = 1000
        elif product == "Tier 2":
            prdt = 1500
        elif product == "Tier 3":
            prdt = 2000
        elif product == "Tier 4":
            prdt = 2500

        duration = 200 * (days - 7)
        customwebhook = 200 if custom_webhook else 0
        channels_cost = (
            0
            if not channels or channels[0] != "♾🔄-unlimited🔄♾"
            else (len(channels) - 1) * 200
        )

        return prdt + duration + customwebhook + channels_cost

    def calculate_giveaway_cost(self, kwargs: dict) -> int:
        product = kwargs.get("product")
        winners = kwargs.get("winners")
        days = kwargs.get("days")
        prizes = kwargs.get("prizes", [])
        use_of_alt_link = kwargs.get("use_of_alt_link")
        use_of_pings = kwargs.get("use_of_pings")

        if product == "Tier 1":
            prdt = 1000
        elif product == "Tier 2":
            prdt = 1250
        elif product == "Tier 3":
            prdt = 1500

        winners_cost = (winners - 1) * 50
        days_cost = (days - 3) * 50
        prizes_cost = 0 if not prizes or prizes[0] == prizes else (len(prizes) * 150)
        alt_link_cost = 100 if use_of_alt_link else 0
        pings_cost = (
            150
            if use_of_pings == "Here"
            else (200 if use_of_pings == "Everyone" else 0)
        )

        return (
            prdt + winners_cost + days_cost + prizes_cost + alt_link_cost + pings_cost
        )

    def calculate_special_servers_cost(self, kwargs: dict) -> int:
        days = kwargs.get("days")
        servers = kwargs.get("servers", "")

        days_cost = (days - 30) * 50
        servers_cost = (len(servers.split(",")) - 1) * 50

        return 1000 + days_cost + servers_cost
