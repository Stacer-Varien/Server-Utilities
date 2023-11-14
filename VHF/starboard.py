from datetime import datetime
from typing import Union
from discord import Color, Embed, Member, Object, Reaction, User
from discord.ext.commands import Bot, Cog


class StarboardCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Union[Member, User]):
        if user.guild.id == 974028573893595146:
            category = user.guild.get_channel(1054090810800472154)
            if reaction.message.channel.id in [i.id for i in category.channels]:
                emoji = next(
                    (
                        i
                        for i in reaction.message.reactions
                        if str(i.emoji) == "❤️" and isinstance(i.emoji, str)
                    ),
                    None,
                )
                if emoji and (emoji.count == 11):
                    starboard = await self.bot.fetch_channel(1173932523764600882)
                    embeds = []

                    image_embeds = [
                        Embed(color=Color.pink())
                        .set_image(url=attachment)
                        .set_footer(
                            text=str(
                                reaction.message.created_at.strftime("%d/%m/%Y %H:%M")
                            )
                        )
                        for attachment in [
                            i.url
                            for i in reaction.message.attachments
                            if i.filename.endswith(("png", "jpeg", "gif", "jpg"))
                        ]
                    ]
                    embeds.extend(image_embeds)

                    video_urls = [
                        i.url
                        for i in reaction.message.attachments
                        if i.filename.endswith(("mp4", "webm"))
                    ]
                    if video_urls:
                        video_embed = Embed(
                            title="Videos", color=Color.pink()
                        ).set_footer(
                            text=str(
                                reaction.message.created_at.strftime("%d/%m/%Y %H:%M")
                            )
                        )
                        video_embed.description = "\n".join(video_urls)
                        embeds.append(video_embed)

                    await starboard.send(embeds=embeds)
                    return


async def setup(bot: Bot):
    await bot.add_cog(StarboardCog(bot), guild=Object(974028573893595146))
