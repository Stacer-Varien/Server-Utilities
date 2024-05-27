import asyncio
from discord import (
    Forbidden,
    Interaction,
    Member,
    Message,
    Object,
    app_commands as serverutil,
    Embed,
    Color,
)
from discord.ext.commands import GroupCog, Bot
from assets.functions import Adwarn
from config import hazead


class AppealCog(GroupCog, name="appeal"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def start_appeal(self, ctx: Interaction, warn_id):
        check_warn = Adwarn().check_id(ctx.user, warn_id)
        if check_warn is None:
            await ctx.followup.send("Invalid warn ID", ephemeral=True)
            return

        appeal_log = ctx.guild.get_channel(951783773006073906)

        try:
            await ctx.followup.send(
                "Let's proceed to your DMs to start the appealing process",
                ephemeral=True,
            )
            await ctx.user.send(
                "Please tell us why we should revoke your warn. Please supply video or images if required.\nYou have 3 minutes to tell"
            )

            def check(m: Message):
                return m.author == ctx.user and (m.attachments or m.content)

            try:
                msg: Message = await self.bot.wait_for(
                    "message", check=check, timeout=180
                )

                await ctx.user.send(
                    "Thank you for appealing for your warn. The appropriate staff member will review it and will send updates if any action is needed\n\nPlease do not rush us or your appeal will be denied."
                )

                reason = check_warn[2]
                moderator = await self.bot.fetch_user(check_warn[1])

                appeal = Embed(title=f"{ctx.user}'s appeal (`{ctx.user.id}`)")
                appeal.add_field(name="Warn ID", value=warn_id, inline=True)
                appeal.add_field(
                    name="Warn reason",
                    value=f"{reason}\nWarned by: {moderator}",
                    inline=False,
                )
                appeal.set_footer(
                    text="To approve the appeal, use `/appeal accept warn_id`"
                )

                try:
                    image_urls = [x.url for x in msg.attachments]
                    images = "\n".join(image_urls)
                    await appeal_log.send(f"{msg.content}\n{images}", embed=appeal)
                except:
                    await appeal_log.send(msg.content, embed=appeal)
            except asyncio.TimeoutError:
                await ctx.user.send("You have run out of time. Please try again.")
        except Forbidden:
            await ctx.followup.send(
                "Please open your DMs to start the appeal process", ephemeral=True
            )

    async def approve_appeal(self, ctx: Interaction, member: Member, warn_id: int):
        if ctx.channel.id == 951783773006073906:
            check_warn = Adwarn().check_id(member, warn_id)
            if check_warn is None:
                await ctx.followup.send("Invalid warn ID", ephemeral=True)
                return

            await Adwarn().remove(member, warn_id)

            try:
                await member.send(
                    f"Hello {member.mention},\nUpon looking into your appeal, we have decided to revoke your warn (**Warn ID:** {warn_id}).\nWe apologize for this and promise that we will be more careful when doing ad moderations against you and other members.\nThank you and enjoy your day!"
                )
            except:
                pass

            await ctx.followup.send(
                "Warning revoked and message sent to member", ephemeral=True
            )

            embed = Embed(color=Color.green())
            embed.description = f"Your adwarn with Warn ID `{warn_id}` has been removed. You now have {Adwarn().points(member)} points"
            adwarn_channel = await member.guild.fetch_channel(925790260695281703)
            await adwarn_channel.send(member.mention, embed=embed)
            return

        await ctx.followup.send(
            "Please do the command in https://ptb.discord.com/channels/925790259160166460/951783773006073906",
            ephemeral=True,
        )

    @serverutil.command(description="Apply for an adwarn appeal")
    @serverutil.describe(warn_id="Insert the warn ID that you wish to appeal your warn")
    async def apply(self, ctx: Interaction, warn_id: int):
        await ctx.response.defer()
        await self.start_appeal(ctx, warn_id)

    @serverutil.command(description="Approve an appeal")
    @serverutil.checks.has_any_role(
        1201835539310059520,
        925790259319558157,
        925790259319558158,
        925790259319558159,
    )
    @serverutil.describe(warn_id="Insert the warn_id ID shown from the member's appeal")
    async def approve(self, ctx: Interaction, member: Member, warn_id: int):
        await ctx.response.defer()
        await self.approve_appeal(ctx, member, warn_id)


async def setup(bot: Bot):
    await bot.add_cog(AppealCog(bot), guild=Object(hazead))
