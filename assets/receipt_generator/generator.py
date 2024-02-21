from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
from discord import Member
from datetime import datetime

class generator:
    def __init__(self) -> None:
        self.font = os.path.join(
            os.path.dirname(__file__), "assets", "receipt_generator", "absender1.ttf"
        )

    def generate_receipt(
        self,
        member: Member,
        type: str,
        product: str,
        custom_webhook: bool = False,
        channels: str = None,#("♾🔄-unlimited🔄♾")
        days: int = 7,
    ):
        if type=="Autoad":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "autoad.png")
            rt_open=Image.open(receipt_template).convert("RGBA")
            draw = ImageDraw.Draw(rt_open)
            # name
            draw.text(
                (610, 540),
                text=member.name,
                font=ImageFont.truetype(self.font, 17),
            )
            # id
            draw.text(
                (610, 660),
                text=str(member.id),
                font=ImageFont.truetype(self.font, 17),
            )
            # date
            draw.text(
                (610, 780),
                text=datetime.now().strftime("%d/%m%Y"),
                font=ImageFont.truetype(self.font, 17),
            )
            # product
            draw.text(
                (610, 900),
                text=product,
                font=ImageFont.truetype(self.font, 17),
            )
            # custom webhook
            draw.text(
                (610, 1110),
                text=str(custom_webhook),
                font=ImageFont.truetype(self.font, 17),
            )
            # days
            draw.text(
                (610, 1180),
                text=str(days),
                font=ImageFont.truetype(self.font, 17),
            )
            # channels
            draw.text(
                (610, 1270),
                text="\n".join(channels),
                font=ImageFont.truetype(self.font, 17),
            )

            # cost
            if product=="Tier 1":
                prdt=1000
            if product == "Tier 2":
                prdt = 1500
            if product == "Tier 3":
                prdt = 2000
            if product == "Tier 4":
                prdt = 2500
            duration = 200 * (days - 7)
            customwebook = 200 if custom_webhook == True else 0
            chnls=(len(channels) - 1) * 200
            total_cost=prdt+duration+customwebook+chnls
            draw.text(
                (870, 2030),
                text=str(total_cost),
                font=ImageFont.truetype(self.font, 17),
            )

            final_bytes = BytesIO()
            rt_open.save(final_bytes, "png")
            final_bytes.seek(0)
            return final_bytes

        if type == "Giveaway":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "giveaway.png")
        if type == "Premium":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "premium.png")
        if type == "SpecialServers":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "specialservers.png")
        if type == "YTNotifier":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "youtubenotifier.png")
