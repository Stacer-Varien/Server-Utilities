import asyncio
import logging
from datetime import datetime, timedelta
from json import load
from pathlib import Path

from discord import (
    Color,
    Embed,
    Forbidden,
    HTTPException,
    Interaction,
    Member,
    Message,
    Object,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog

from assets.components import YesNoButtons
from assets.functions import Verification
from config import vhf

logger = logging.getLogger(__name__)


class VerificationCog(GroupCog, name="verification"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.context_menus = [
            Serverutil.ContextMenu(
                name="Approve Verification", callback=self.approve_verification
            ),
            Serverutil.ContextMenu(
                name="Deny Verification", callback=self.deny_verification
            ),
            Serverutil.ContextMenu(
                name="Force Verification", callback=self.force_verification
            ),
        ]
        guild = Object(vhf)
        for command in self.context_menus:
            self.bot.tree.add_command(command, guild=guild)

    def cog_unload(self) -> None:
        guild = Object(vhf)
        for command in self.context_menus:
            self.bot.tree.remove_command(command.name, guild=guild, type=command.type)

    async def get_request_member(
        self, message: Message, verification: Verification
    ) -> Member | None:
        if message.guild is None:
            return None

        user_id = verification.get_request_user_id(message)
        if user_id is None:
            return None

        member = message.guild.get_member(user_id)
        if member is not None:
            return member

        try:
            return await message.guild.fetch_member(user_id)
        except HTTPException:
            return None

    async def approve_deny_common(
        self, ctx: Interaction, message: Message, approved: bool
    ):
        await ctx.response.defer(ephemeral=True)
        verification = Verification()
        embed = Embed(color=Color.random())

        if not verification.has_request_for_message(message):
            embed.description = "This member hasn't requested verification yet."
            embed.color = Color.red()
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        member = await self.get_request_member(message, verification)
        if member is None:
            embed.description = (
                "Could not find the member for this verification request."
            )
            embed.color = Color.red()
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        if approved:
            await verification.approve(message, member)
        else:
            await verification.deny(message)

        outcome = "approved" if approved else "denied"
        try:
            dm_embed = Embed(
                description=(
                    f"Hi {member}\nYour verification has been {outcome} "
                    f"in {ctx.guild.name}!"
                ),
                color=Color.random(),
            )
            dm_embed.set_footer(
                text=(
                    "Verification does not mean instant NSFW access. "
                    "It is your choice to view it or not."
                )
            )
            await member.send(embed=dm_embed)
        except HTTPException:
            pass

        embed.description = f"{member} has been {outcome}."
        await ctx.followup.send(embed=embed, ephemeral=True)
        await self.send_verification_log(
            title=f"Verification Log ({outcome.title()})",
            member=member,
            moderator=ctx.user,
        )

        try:
            await message.delete(delay=5)
        except HTTPException:
            pass

    async def send_verification_log(
        self, title: str, member: Member, moderator: Member
    ):
        embed = Embed(title=title)
        embed.add_field(name="Member", value=str(member), inline=False)
        embed.add_field(name="ID", value=str(member.id), inline=False)
        embed.add_field(name="Moderator", value=str(moderator), inline=False)
        embed.add_field(name="Moderator ID", value=str(moderator.id), inline=False)
        embed.add_field(
            name="Date and Time",
            value=f"<t:{round(datetime.now().timestamp())}:F>",
            inline=False,
        )

        try:
            verification_log = await self.bot.fetch_channel(991655158930997358)
            await verification_log.send(embed=embed)
        except HTTPException:
            logger.exception("Could not send verification log for member %s", member.id)

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def approve_verification(self, ctx: Interaction, message: Message):
        await self.approve_deny_common(ctx, message, approved=True)

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def deny_verification(self, ctx: Interaction, message: Message):
        await self.approve_deny_common(ctx, message, approved=False)

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def force_verification(self, ctx: Interaction, member: Member):
        await ctx.response.defer(ephemeral=True)
        embed = Embed(color=Color.red())
        verification = Verification()

        if verification.has_request_for_member(member):
            embed.description = f"{member} already requested an ID verification."
            await ctx.followup.send(embed=embed, ephemeral=True)
            return
        if verification.is_verified(member):
            embed.description = f"{member} is already verified."
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        if not await verification.force(member):
            embed.description = "The configured untrusted role could not be found."
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        verify_here = await member.guild.fetch_channel(1059903781552267294)

        notice = Embed(
            description="""
You have been forced to do verification due to one of the following reasons:

1. You are suspected to be underage
2. You were joking about your age
3. You might be impersonating someone
4. You may be a selfbot or userbot

All removable roles have been removed and the untrusted role has been added.
""",
            color=Color.red(),
        )
        notice.add_field(
            name="How to start verification?",
            value=(
                f"Type `/verification start` in {verify_here.jump_url}. "
                "Make sure your DMs are temporarily open."
            ),
            inline=False,
        )
        notice.add_field(
            name="What happens if I don't verify?",
            value=(
                "You have 48 hours to successfully verify, or you may be banned. "
                "This only applies to people who are forced to verify."
            ),
            inline=False,
        )
        notice.add_field(
            name="What happens after verification?",
            value=(
                "The untrusted role will be removed and the verified member roles "
                "will be added. Other roles must be selected again."
            ),
            inline=False,
        )

        try:
            await member.send(embed=notice)
        except HTTPException:
            await verify_here.send(content=member.mention, embed=notice)

        log_embed = Embed(title="Notice of Force Verification")
        log_embed.add_field(name="Member", value=str(member), inline=False)
        log_embed.add_field(name="ID", value=str(member.id), inline=False)
        log_embed.add_field(name="Notice by", value=str(ctx.user), inline=False)
        log_embed.add_field(name="Moderator ID", value=str(ctx.user.id), inline=False)
        log_embed.add_field(
            name="Ban availability",
            value=f"<t:{round((datetime.now() + timedelta(hours=48)).timestamp())}:R>",
            inline=False,
        )

        try:
            verification_log = await self.bot.fetch_channel(991655158930997358)
            await verification_log.send(embed=log_embed)
        except HTTPException:
            logger.exception(
                "Could not send force-verification log for member %s", member.id
            )

        embed.description = f"Forced verification notice sent to {member}."
        embed.color = Color.green()
        await ctx.followup.send(embed=embed, ephemeral=True)

    @Serverutil.command(name="start", description="Start the verification process")
    async def start_verification(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        embed = Embed(color=Color.red())

        if ctx.guild is None or not isinstance(ctx.user, Member):
            embed.description = "This command can only be used in the server."
            await ctx.edit_original_response(embed=embed)
            return

        verification = Verification()
        if verification.has_request_for_member(ctx.user):
            embed.description = "You have already requested an ID verification."
            await ctx.edit_original_response(embed=embed)
            return
        if verification.is_verified(ctx.user):
            embed.description = "You are already verified."
            await ctx.edit_original_response(embed=embed)
            return

        json_path = (
            Path(__file__).resolve().parents[1] / "assets" / "verification_process.json"
        )
        with json_path.open("r", encoding="utf-8") as file:
            json_data = load(file)

        try:
            intro_message = await ctx.user.send(
                embed=Embed.from_dict(json_data["embeds"][0])
            )
            view = YesNoButtons(author=ctx.user)
            prompt_embed = Embed(
                description=(
                    "Have you read the steps and met the requirements? "
                    "Choose No if you need more time."
                )
            )
            prompt_embed.set_footer(text="These buttons time out after 10 minutes.")
            prompt = await ctx.user.send(embed=prompt_embed, view=view)
        except Forbidden:
            embed.description = (
                "Please temporarily open your DMs to start verification."
            )
            await ctx.edit_original_response(embed=embed)
            return

        await ctx.edit_original_response(
            embed=Embed(
                description=f"Continue the verification process in {intro_message.jump_url}."
            )
        )
        await view.wait()
        await prompt.edit(view=None)

        if view.value is not True:
            embed.description = (
                "Verification was cancelled or timed out. Please try again."
            )
            await prompt.edit(embed=embed)
            await ctx.edit_original_response(embed=embed)
            return

        image_urls = []

        def is_image_message(message: Message):
            return (
                message.author.id == ctx.user.id
                and message.channel.id == prompt.channel.id
                and bool(message.attachments)
            )

        for step in json_data["steps"]:
            step_embed = Embed(description=step)
            await prompt.edit(embed=step_embed)

            try:
                message = await self.bot.wait_for(
                    "message", check=is_image_message, timeout=600
                )
            except asyncio.TimeoutError:
                embed.description = (
                    "Timed out waiting for an image. Please restart verification."
                )
                await prompt.edit(embed=embed)
                await ctx.edit_original_response(embed=embed)
                return

            image = next(
                (
                    attachment
                    for attachment in message.attachments
                    if (
                        attachment.content_type
                        and attachment.content_type.startswith("image/")
                    )
                    or attachment.filename.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".webp")
                    )
                ),
                None,
            )
            if image is None:
                embed.description = "That attachment is not a supported image. Please restart verification."
                await prompt.edit(embed=embed)
                await ctx.edit_original_response(embed=embed)
                return
            image_urls.append(image.url)

        request_embed = Embed(title="Verification images", color=Color.random())
        for index, image_url in enumerate(image_urls, start=1):
            request_embed.add_field(
                name=f"Image {index}", value=f"[Open image]({image_url})", inline=False
            )

        try:
            verification_channel = await self.bot.fetch_channel(1055487338500857946)
            request = await verification_channel.send(
                content=f"New request from {ctx.user} `{ctx.user.id}`",
                embed=request_embed,
            )
            if not await verification.add_request(ctx.user, request):
                try:
                    await request.delete()
                except HTTPException:
                    logger.warning(
                        "Could not remove duplicate verification request %s",
                        request.id,
                    )

                embed.description = (
                    "You already have a verification request pending. "
                    "Please wait for staff to review it."
                )
                await prompt.edit(embed=embed)
                await ctx.edit_original_response(embed=embed)
                return
        except HTTPException:
            logger.exception("Could not submit verification for member %s", ctx.user.id)
            embed.description = (
                "Your verification could not be submitted. Please try again later."
            )
            await prompt.edit(embed=embed)
            await ctx.edit_original_response(embed=embed)
            return

        complete = Embed(
            description=(
                "Your verification request was sent to authorized staff. "
                "Do not delete the submitted images until you receive an outcome."
            ),
            color=Color.green(),
        )
        await prompt.edit(embed=complete)
        await ctx.edit_original_response(embed=complete)


async def setup(bot: Bot):
    await bot.add_cog(VerificationCog(bot), guild=Object(vhf))
