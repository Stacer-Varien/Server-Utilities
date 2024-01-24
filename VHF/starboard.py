from discord import (
    Color,
    Embed,
    Emoji,
    Message,
    Object,
    RawReactionActionEvent,
)
from discord.ext.commands import Bot, Cog


class StarboardCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        with open("message_ids.txt", "r") as f:
            message_ids = f.read().split("\n")

        guild_id = 974028573893595146
        if payload.member.guild.id == guild_id:
            events = payload.member.guild.get_channel(1054090810800472154)
            categories = [
                events,
                payload.member.guild.get_channel(985976523607650415),
                payload.member.guild.get_channel(1194627560294842399),
                payload.member.guild.get_channel(1194629375207952505),
                payload.member.guild.get_channel(1165684137735241840),
                payload.member.guild.get_channel(1194632735453630565),
            ]

            if payload.channel_id in [
                i.id
                for i in events.channels
                if i.id not in (1179067756918882386, 1181566295540518992)
            ]:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message: Message = await channel.fetch_message(payload.message_id)
                emoji = next(
                    (
                        i
                        for i in message.reactions
                        if isinstance(i.emoji, Emoji)
                        and i.emoji.name == "mhxaLove"
                        and i.emoji.id == 1174261737697050625
                    ),
                    None,
                )

                if (
                    emoji
                    and emoji.count == 3
                    and str(payload.message_id) not in message_ids
                ):
                    with open("message_ids.txt", "a") as f:
                        f.writelines(f"{payload.message_id}\n")
                    starboard = await self.bot.fetch_channel(1173932523764600882)
                    embeds = []

                    image_embeds = [
                        Embed(description=message.channel.mention, color=Color.pink())
                        .set_image(url=attachment.url)
                        .set_footer(
                            text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                        )
                        for attachment in message.attachments
                        if attachment.filename.endswith(("png", "jpeg", "gif", "jpg"))
                    ]
                    embeds.extend(image_embeds)

                    video_urls = [
                        attachment.url
                        for attachment in message.attachments
                        if attachment.filename.endswith(("mp4", "webm"))
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

            if payload.channel_id in [i.id for i in categories]:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message: Message = await channel.fetch_message(payload.message_id)

                if bool(message.attachments) and len(message.attachments) >= 1:
                    emoji = next(
                        (
                            i
                            for i in message.reactions
                            if isinstance(i.emoji, Emoji)
                            and i.emoji.name == "mhxaLove"
                            and i.emoji.id == 1174261737697050625
                        ),
                        None,
                    )
                    if (
                        emoji
                        and emoji.count == 5
                        and payload.message_id not in message_ids
                    ):
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
                            .set_image(url=attachment.url)
                            .set_footer(
                                text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                            )
                            for attachment in message.attachments
                            if attachment.filename.endswith(
                                ("png", "jpeg", "gif", "jpg")
                            )
                        ]
                        embeds.extend(image_embeds)

                        video_urls = [
                            attachment.url
                            for attachment in message.attachments
                            if attachment.filename.endswith(("mp4", "webm"))
                        ]
                        if video_urls:
                            video_embed = Embed(
                                title=f"Posted by {message.author}",
                                title=f"Videos from {message.channel.mention}",
                                color=Color.pink(),
                            ).set_footer(
                                text=str(message.created_at.strftime("%d/%m/%Y %H:%M"))
                            )
                            video_embed.description = "\n".join(video_urls)
                            embeds.append(video_embed)

                        await starboard.send(embeds=embeds)


async def setup(bot: Bot):
    await bot.add_cog(StarboardCog(bot), guild=Object(974028573893595146))
