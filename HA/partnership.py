import os
from discord import Color, Embed, Interaction, Member, Message, Object, app_commands as Serverutil
from discord.ext.commands import GroupCog, Bot
from assets.functions import Partner
from config import hazead, orleans

# ha
partner_manager = 925790259319558155
admins = 925790259319558157
owner = 925790259319558159

# orleans
management = 762318708596015114


class partnercog(GroupCog, name="partner"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Parter with Orleans")
    async def apply(self, ctx: Interaction):
        await ctx.response.defer()
        dm_link = await ctx.user.send(
            "Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite."
        )
        await ctx.followup.send(
            f"Please go to your [DMs]({dm_link.jump_url}) to proceed with the partnership"
        )

        def check(m: Message):
            return m.author == ctx.user and m.content

        try:
            ad: Message = await self.bot.wait_for("message", check=check, timeout=180)

            if ctx.guild.id == 740584420645535775:
                with open("HA/orleans.txt", "r") as f:
                    content = "".join(f.readlines())

            elif ctx.guild.id == 925790259160166460:
                with open("HA/hazeads.txt", "r") as f:
                    content = "".join(f.readlines())

            await ctx.user.send(content)
            await ctx.user.send(
                "We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot with date and time showing as proof. This is just to avoid partnership scams"
            )

            try:

                def check_image(m: Message):
                    return m.author == ctx.user and m.attachments

                proof: Message = await self.bot.wait_for(
                    "message", check=check_image, timeout=180
                )

                image_urls = [x.url for x in proof.attachments]
                images = "\n".join(image_urls)

                if ctx.guild.id == 740584420645535775:
                    with open(
                        "partnerships/orleans/{}.txt".format(ctx.user.id), "w"
                    ) as f:
                        f.write(ad.content)
                    partnerchannel = self.bot.get_channel(1051048278181031988)

                elif ctx.guild.id == 925790259160166460:
                    with open(
                        "partnerships/hazeads/{}.txt".format(ctx.user.id), "w"
                    ) as f:
                        f.write(ad.content)
                    partnerchannel = self.bot.get_channel(981877384192094279)

                await ctx.user.send(
                    "Partnership is now complete. Please wait for a response from us that your partnership request is accepted or denied"
                )

                await partnerchannel.send("```{}```".format(ad.content))

                request = Embed(
                    title="Partnership for Orleans",
                    description="To approve or deny the partnership, use `/partner approve MEMBER` or `/partner deny MEMBER REASON`",
                    color=Color.blue(),
                )
                request.set_footer(
                    text=f"Partnership request by {ctx.user}\nPartnership ID: {ctx.user.id}"
                )

                await partnerchannel.send(
                    f"Proof they have posted our ad : {images}", embed=request
                )
            except TimeoutError:
                await ctx.user.send("You have ran out of time. Please try again later")
        except TimeoutError:
            await ctx.user.send("You have ran out of time. Please try again later")

    @Serverutil.command(description="Approve a partnership")
    @Serverutil.checks.has_any_role(partner_manager, admins, owner, management)
    async def approve(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        partner = Partner(member, ctx.guild)
        if partner.check() == True:
            await partner.approve(ctx)

    @Serverutil.command(description="Deny a partnership")
    @Serverutil.describe(
        reason="What was the reason for denying the partnership request?"
    )
    @Serverutil.checks.has_any_role(partner_manager, admins, owner)
    async def deny(self, ctx: Interaction, member: Member, reason: str):
        await ctx.response.defer()
        partner = Partner(member, ctx.guild)
        if partner.check() == True:
            await partner.deny(ctx, reason)


async def setup(bot: Bot):
    await bot.add_cog(partnercog(bot), guilds=[Object(id=hazead), Object(id=orleans)])
