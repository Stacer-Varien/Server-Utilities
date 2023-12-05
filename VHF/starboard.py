from datetime import datetime
from typing import Union
from discord import (
    Color,
    Embed,
    Emoji,
    Member,
    Message,
    Object,
    RawReactionActionEvent,
    Reaction,
    User,
)
from discord.ext.commands import Bot, Cog


class StarboardCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        with open("message_ids.txt", "r") as f:
            message_ids=f.read().split("\n")    
        if payload.member.guild.id == 974028573893595146:
            category = payload.member.guild.get_channel(1054090810800472154)
            alt_hentai = payload.member.guild.get_channel(1165684137735241840)
            non_alt = payload.member.guild.get_channel(985976523607650415)
            if payload.channel_id in [
                i.id for i in category.channels if not (i.id == 1179067756918882386)
            ]:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message: Message = await channel.fetch_message(payload.message_id)
                emoji = [
                    i
                    for i in message.reactions
                    if isinstance(i.emoji, Emoji)
                    and i.emoji.name == "mhxaLove"
                    and i.emoji.id == 1174261737697050625
                ][0]
                if emoji.count == 3:
                    if str(payload.message_id) in message_ids:
                        return
                    with open("message_ids.txt", "a") as f:
                        f.writelines(f"{payload.message_id}\n")                
                    starboard = await self.bot.fetch_channel(1173932523764600882)
                    embeds = []

                    image_embeds = [
                        Embed(
                            description=message.channel.mention,
                            color=Color.pink(),
                        )
                        .set_image(url=attachment)
                        .set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        for attachment in [
                            i.url
                            for i in message.attachments
                            if i.filename.endswith(("png", "jpeg", "gif", "jpg"))
                        ]
                    ]
                    embeds.extend(image_embeds)

                    video_urls = [
                        i.url
                        for i in message.attachments
                        if i.filename.endswith(("mp4", "webm"))
                    ]
                    if video_urls:
                        video_embed = Embed(
                            title=f"Videos from {message.channel.mention}",
                            color=Color.pink(),
                        ).set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        video_embed.description = "\n".join(video_urls)
                        embeds.append(video_embed)

                    await starboard.send(embeds=embeds)
                    return

            if payload.channel_id in [i.id for i in non_alt.channels]:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message: Message = await channel.fetch_message(payload.message_id)
                emoji = [i for i in message.reactions if i.emoji == "🎄"][0]
                if emoji.count == 5:
                    if payload.message_id in message_ids:
                        return
                    with open("message_ids.txt", "a") as f:
                        f.writelines(f"{payload.message_id}\n")                
                    starboard = await self.bot.fetch_channel(1173932523764600882)
                    embeds = []

                    image_embeds = [
                        Embed(
                            title=f"Posted by {message.author}",
                            description=message.channel.mention,
                            color=Color.pink(),
                        )
                        .set_image(url=attachment)
                        .set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        for attachment in [
                            i.url
                            for i in message.attachments
                            if i.filename.endswith(("png", "jpeg", "gif", "jpg"))
                        ]
                    ]
                    embeds.extend(image_embeds)

                    video_urls = [
                        i.url
                        for i in message.attachments
                        if i.filename.endswith(("mp4", "webm"))
                    ]
                    if video_urls:
                        video_embed = Embed(
                            f"Posted by {message.author}",
                            title=f"Videos from {message.channel.mention}",
                            color=Color.pink(),
                        ).set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        video_embed.description = "\n".join(video_urls)
                        embeds.append(video_embed)

                    await starboard.send(embeds=embeds)
                    return

            if payload.channel_id in [i.id for i in alt_hentai.channels]:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message: Message = await channel.fetch_message(payload.message_id)
                emoji = [i for i in message.reactions if i.emoji == "🎄"][0]
                if emoji.count == 5:
                    if payload.message_id in message_ids:
                        return
                    with open("message_ids.txt", "a") as f:
                        f.writelines(f"{payload.message_id}\n")                
                    starboard = await self.bot.fetch_channel(1173932523764600882)
                    embeds = []

                    image_embeds = [
                        Embed(
                            title=f"Posted by {message.author}",
                            description=message.channel.mention,
                            color=Color.pink(),
                        )
                        .set_image(url=attachment)
                        .set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        for attachment in [
                            i.url
                            for i in message.attachments
                            if i.filename.endswith(("png", "jpeg", "gif", "jpg"))
                        ]
                    ]
                    embeds.extend(image_embeds)

                    video_urls = [
                        i.url
                        for i in message.attachments
                        if i.filename.endswith(("mp4", "webm"))
                    ]
                    if video_urls:
                        video_embed = Embed(
                            f"Posted by {message.author}",
                            title=f"Videos from {message.channel.mention}",
                            color=Color.pink(),
                        ).set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        video_embed.description = "\n".join(video_urls)
                        embeds.append(video_embed)

                    await starboard.send(embeds=embeds)
                    return


async def setup(bot: Bot):
    await bot.add_cog(StarboardCog(bot), guild=Object(974028573893595146))
