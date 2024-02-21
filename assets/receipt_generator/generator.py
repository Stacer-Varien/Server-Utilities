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
        channels: str = "♾🔄-unlimited🔄♾",
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
                font=ImageFont.truetype(self.font, 20),
            )
            # id
            draw.text(
                (610, 660),
                text=str(member.id),
                font=ImageFont.truetype(self.font, 20),
            )
            # date
            draw.text(
                (610, 540),
                text=datetime.now().strftime("%d/%m%Y"),
                font=ImageFont.truetype(self.font, 20),
            )
            # product
            draw.text(
                (610, 540),
                text=product,
                font=ImageFont.truetype(self.font, 20),
            )
            # custom webhook
            draw.text(
                (610, 540),
                text=str(custom_webhook),
                font=ImageFont.truetype(self.font, 20),
            )
            # days
            draw.text(
                (610, 540),
                text=str(days),
                font=ImageFont.truetype(self.font, 20),
            )
            #channels
            draw.text(
                (610, 540),
                text=str(channels),
                font=ImageFont.truetype(self.font, 20),
            )

        if type == "Giveaway":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "giveaway.png")
        if type == "Premium":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "premium.png")
        if type == "SpecialServers":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "specialservers.png")
        if type == "YTNotifier":
            receipt_template = os.path.join(os.path.dirname(__file__), "assets", "receipt_generator", "youtubenotifier.png")
