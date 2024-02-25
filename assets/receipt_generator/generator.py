from io import BytesIO
import os
from random import randint
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
from discord import Interaction, Member
from datetime import datetime

from assets.functions import Currency


class generator:
    def __init__(self) -> None:
        self.font = os.path.join(os.path.dirname(__file__), "absender1.ttf")

    async def generate_receipt(
        self,
        ctx: Interaction,
        member: Member,
        type: str,
        product: str,
        custom_webhook: Optional[bool] = False,
        channels: Optional[list[str]] = None,
        days: Optional[int] = 7,
        winners: Optional[int] = 1,
        prizes: Optional[list[str]] = None,
        use_of_pings: Optional[str] = None,
        use_of_alt_link: Optional[bool] = False,
    ):
        bank_instance=Currency(member)
        if type == "Autoad":
            receipt_template = os.path.join(os.path.dirname(__file__), "autoad.png")
            rt_open = Image.open(receipt_template).convert("RGBA")
            draw = ImageDraw.Draw(rt_open)
            # transaction ID
            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # name
            draw.text(
                (610, 540),
                text=member.name,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # id
            draw.text(
                (610, 700),
                text=str(member.id),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # date
            draw.text(
                (610, 820),
                text=datetime.now().strftime("%d/%m%Y"),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # product
            draw.text(
                (610, 950),
                text=product,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # custom webhook
            draw.text(
                (610, 1110),
                text=str(custom_webhook),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # days
            draw.text(
                (610, 1170),
                text=str(days),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # channels
            draw.text(
                (610, 1260),
                text="\n".join(channels),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )

            # cost
            if product == "Tier 1":
                prdt = 1000
            if product == "Tier 2":
                prdt = 1500
            if product == "Tier 3":
                prdt = 2000
            if product == "Tier 4":
                prdt = 2500
            duration = 200 * (days - 7)
            customwebook = 200 if custom_webhook == True else 0
            chnls = (
                0
                if not channels or channels[0] != "♾🔄-unlimited🔄♾"
                else (len(channels) - 1) * 200
            )

            total_cost = prdt + duration + customwebook + chnls
            if bank_instance.get_balance < total_cost:
                await ctx.edit_original_response("Your balance is too low. Please try again when you have sufficient funds")
                return

            draw.text(
                (870, 2030),
                text=str(total_cost),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )

        if type == "Giveaway":
            receipt_template = os.path.join(
                os.path.dirname(__file__), "assets", "receipt_generator", "giveaway.png"
            )
            rt_open = Image.open(receipt_template).convert("RGBA")
            draw = ImageDraw.Draw(rt_open)
            #costs
            if product == "Tier 1":
                prdt = 1000
            if product == "Tier 2":
                prdt = 1250
            if product == "Tier 3":
                prdt = 1500
            # transaction ID
            draw.text(
                (1260, 290),
                text=str(randint(0, 99999)),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # name
            draw.text(
                (640, 540),
                text=member.name,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # id
            draw.text(
                (640, 700),
                text=str(member.id),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # date
            draw.text(
                (640, 820),
                text=datetime.now().strftime("%d/%m%Y"),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # product
            draw.text(
                (640, 950),
                text=product,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # winners
            draw.text(
                (640, 1120),
                text=winners,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # required
            draw.text(
                (640, 1210),
                text="Yes",
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # alt link
            draw.text(
                (640, 1300),
                text=use_of_alt_link,
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
            # prizes
            if prizes==None:
                prizes=f"As required in {product}"
            draw.text(
                (640, 1460),
                text="\n".join(prizes),
                fill=(0, 0, 0),
                font=ImageFont.truetype(self.font, 60),
            )
        if type == "Premium":
            receipt_template = os.path.join(
                os.path.dirname(__file__), "assets", "receipt_generator", "premium.png"
            )
        if type == "SpecialServers":
            receipt_template = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "receipt_generator",
                "specialservers.png",
            )
        if type == "YTNotifier":
            receipt_template = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "receipt_generator",
                "youtubenotifier.png",
            )

        final_bytes = BytesIO()
        rt_open.save(final_bytes, "png")
        final_bytes.seek(0)
        await bank_instance.remove_credits(total_cost)
        return final_bytes
