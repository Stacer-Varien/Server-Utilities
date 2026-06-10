import asyncio
import logging

from discord import (
    ButtonStyle,
    Color,
    Embed,
    HTTPException,
    Object,
    RawReactionActionEvent,
    ui,
)
from discord.ext.commands import Bot, Cog

from config import BASE_DIR, db, vhf

logger = logging.getLogger(__name__)


class ReactionCog(Cog):
    LOVE_EMOJI_NAME = "mhxaLove"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.role_channel_id = 1115725010649235608
        self.starboard_channel_id = 1173932523764600882
        self.emoji_roles = {
            "🌈": 1115726474318729257,
            "🎃": 1153989722327228486,
            "🧝": None,
            "🖐️": 1200443228395147295,
            "🎄": 1311776856432836648,
        }
        self.starboard_lock = asyncio.Lock()
        self.migrate_starboard_ids()

    def migrate_starboard_ids(self):
        legacy_path = BASE_DIR / "message_ids.txt"
        if not legacy_path.exists():
            return

        message_ids = [
            int(value)
            for value in legacy_path.read_text(encoding="utf-8").splitlines()
            if value.isdigit()
        ]
        db.executemany(
            """
            INSERT OR IGNORE INTO starboardPosts (message_id, starboard_message_id)
            VALUES (?, 0)
            """,
            ((message_id,) for message_id in message_ids),
        )
        db.commit()

    async def handle_role_reaction(self, payload: RawReactionActionEvent):
        if (
            payload.guild_id != vhf
            or payload.channel_id != self.role_channel_id
            or (self.bot.user and payload.user_id == self.bot.user.id)
        ):
            return

        role_id = self.emoji_roles.get(str(payload.emoji))
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        member = payload.member or guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except HTTPException:
                return

        role = guild.get_role(role_id)
        if role is None:
            return

        try:
            if payload.event_type == "REACTION_ADD":
                await member.add_roles(role, reason="Reaction role added")
            elif payload.event_type == "REACTION_REMOVE":
                await member.remove_roles(role, reason="Reaction role removed")
        except HTTPException:
            logger.warning(
                "Could not update reaction role %s for member %s", role_id, member.id
            )

    async def handle_starboard_reaction(self, payload: RawReactionActionEvent):
        if (
            payload.guild_id != vhf
            or payload.channel_id == self.role_channel_id
            or payload.emoji.name != self.LOVE_EMOJI_NAME
            or (self.bot.user and payload.user_id == self.bot.user.id)
        ):
            return

        async with self.starboard_lock:
            already_posted = db.execute(
                "SELECT 1 FROM starboardPosts WHERE message_id = ?",
                (payload.message_id,),
            ).fetchone()
            if already_posted:
                return

            try:
                channel = await self.bot.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
            except HTTPException:
                return

            reaction = next(
                (
                    item
                    for item in message.reactions
                    if getattr(item.emoji, "name", str(item.emoji))
                    == self.LOVE_EMOJI_NAME
                ),
                None,
            )
            if reaction is None or reaction.count < 3:
                return

            content = (message.content or "").strip()
            content_snippet = content[:1000]
            description = f"{message.channel.mention} by *{message.author}*"
            if content_snippet:
                description += f"\n\n{content_snippet}"

            embeds = []
            for attachment in message.attachments:
                filename = attachment.filename.lower()
                if filename.endswith((".png", ".jpeg", ".gif", ".jpg", ".webp")):
                    embed = Embed(description=description, color=Color.pink())
                    embed.set_image(url=attachment.url)
                    embeds.append(embed)
                elif filename.endswith((".mp4", ".webm", ".mov")):
                    embed = Embed(
                        title=f"Video from {message.channel.mention}",
                        description=f"{description}\n\n{attachment.url}",
                        color=Color.pink(),
                    )
                    embeds.append(embed)

                if len(embeds) == 10:
                    break

            if not embeds:
                embeds.append(Embed(description=description, color=Color.pink()))

            for embed in embeds:
                embed.set_footer(text=message.created_at.strftime("%d/%m/%Y %H:%M"))

            view = ui.View(timeout=None)
            view.add_item(
                ui.Button(
                    label="Jump to message",
                    style=ButtonStyle.url,
                    url=message.jump_url,
                )
            )

            try:
                starboard = await self.bot.fetch_channel(self.starboard_channel_id)
                starboard_message = await starboard.send(embeds=embeds, view=view)
            except HTTPException:
                logger.exception("Could not send message %s to starboard", message.id)
                return

            db.execute(
                """
                INSERT INTO starboardPosts (message_id, starboard_message_id)
                VALUES (?, ?)
                """,
                (message.id, starboard_message.id),
            )
            db.commit()

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.handle_role_reaction(payload)
        await self.handle_starboard_reaction(payload)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.handle_role_reaction(payload)


async def setup(bot: Bot):
    await bot.add_cog(ReactionCog(bot), guild=Object(vhf))
