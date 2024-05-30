from discord import Color, Embed, Emoji, Object, RawReactionActionEvent
from discord.ext.commands import Bot, Cog
from config import vhf


class ReactionCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.role_channel_id = 1115725010649235608
        self.starboard_channel_id = 1173932523764600882
        self.emoji_roles = {
            "🌈": 1115726474318729257,
            "🎃": 1153989722327228486,
            "🧝": None,
            "🖐️": 1200443228395147295,
        }

    async def handle_role_reaction(self, payload: RawReactionActionEvent):
        if payload.channel_id == self.role_channel_id:
            role_id = self.emoji_roles.get(str(payload.emoji))
            if role_id:
                role = payload.member.guild.get_role(role_id)
                if role:
                    if payload.event_type == "REACTION_ADD":
                        await payload.member.add_roles(role)
                    elif payload.event_type == "REACTION_REMOVE":
                        await payload.member.remove_roles(role)

    async def handle_starboard_reaction(self, payload: RawReactionActionEvent):
        if payload.channel_id != self.role_channel_id:
            message_ids_file = "message_ids.txt"
            with open(message_ids_file, "r") as f:
                message_ids = f.read().splitlines()

            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            emoji_name = "mhxaLove"

            if (
                payload.event_type == "REACTION_ADD"
                and str(message.id) not in message_ids
            ):
                emoji = next(
                    (
                        i
                        for i in message.reactions
                        if isinstance(i.emoji, Emoji) and i.emoji.name == emoji_name
                    ),
                    None,
                )
                if emoji and emoji.count in [3, 5]:
                    with open(message_ids_file, "a") as f:
                        f.write(f"{message.id}\n")
                    starboard = await self.bot.fetch_channel(self.starboard_channel_id)
                    embeds = []

                    for attachment in message.attachments:
                        if attachment.filename.endswith(("png", "jpeg", "gif", "jpg")):
                            embed = Embed(
                                description=message.channel.mention, color=Color.pink()
                            )
                            embed.set_image(url=attachment.url)
                            embed.set_footer(
                                text=message.created_at.strftime("%d/%m/%Y %H:%M")
                            )
                            embeds.append(embed)
                        elif attachment.filename.endswith(("mp4", "webm")):
                            video_embed = Embed(
                                title=f"Videos from {message.channel.mention}",
                                color=Color.pink(),
                            )
                            video_embed.description = attachment.url
                            video_embed.set_footer(
                                text=message.created_at.strftime("%d/%m/%Y %H:%M")
                            )
                            embeds.append(video_embed)

                    await starboard.send(embeds=embeds)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.handle_role_reaction(payload)
        await self.handle_starboard_reaction(payload)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.handle_role_reaction(payload)


async def setup(bot: Bot):
    await bot.add_cog(ReactionCog(bot), guild=Object(vhf))
