from asyncio import TimeoutError
from discord import app_commands as serverutil
from discord import Interaction, Embed, Object
from discord.ext.commands import GroupCog, Bot
from assets.functions import Warn, Appeal
from config import hazead
from discord import Message


class appealcog(GroupCog, name="appeal"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @serverutil.command(description="Apply for an adwarn appeal")
    @serverutil.describe(warn_id="Insert the warn ID that you want to appeal")
    async def apply(self, ctx: Interaction, warn_id: int):
        await ctx.response.defer()
        check_warn = Warn(ctx.user, warn_id).check_warn()
        if check_warn == None:
            await ctx.followup.send("Invalid warn ID", ephemeral=True)

        else:
            appeal_log = ctx.guild.get_channel(951783773006073906)

            try:
                await ctx.followup.send(
                    "Please make sure your DMs are opened to start the appealing process",
                    ephemeral=True,
                )

                await ctx.user.send(
                    "Please tell us why we should revoke your warn. Please supply video or images if required.\nYou have 3 minutes to tell"
                )

                def check(m: Message):
                    attachments = bool(m.attachments)
                    content = bool(m.content)
                    if attachments == True and content == True:
                        return m.author == ctx.user and m.content and m.attachments
                    elif content == True:
                        return m.author == ctx.user and m.content
                    elif attachments == True:
                        return m.author == ctx.user and m.attachments
                    elif attachments == True and content == False:
                        return m.author == ctx.user and m.attachments

                try:
                    msg: Message = await self.bot.wait_for(
                        "message", check=check, timeout=180
                    )

                    await ctx.user.send(
                        "Thank you for appealing for your warn. The appropriate staff member will review it and will send updates if any action is needed\nPlease do not rush us or your appeal will be denied."
                    )

                    reason = check_warn[2]
                    moderator = await self.bot.fetch_user(check_warn[1])
                    appeal_id = check_warn[4]

                    appeal = Embed(title=f"{ctx.user}'s appeal")
                    appeal.add_field(name="Warn ID", value=warn_id, inline=True)
                    appeal.add_field(name="Appeal ID", value=appeal_id, inline=True)
                    appeal.add_field(
                        name="Warn reason", value=f"{reason}\nWarned by: {moderator}"
                    )
                    appeal.add_field(
                        name="How to approve or deny?",
                        value=f"{reason}\nWarned by: {moderator}",
                    )
                    appeal.set_footer(
                        text="To approve the appeal, use `/verdict accept appeal_id`. To deny the appeal, use `/verdict deny appeal_id`"
                    )

                    try:
                        image_urls = [x.url for x in msg.attachments]
                        images = "\n".join(image_urls)
                        await appeal_log.send(
                            "{}\n{}".format(msg, images), embed=appeal
                        )
                    except:
                        await appeal_log.send(msg, embed=appeal)
                except TimeoutError:
                    await ctx.user.send("You have ran out of time. Please try again.")
            except:
                await ctx.followup.send(
                    "Please open your DMs to start the appeal process", ephemeral=True
                )

    @serverutil.command(description="Approve an appeal")
    @serverutil.checks.has_role(925790259319558157)
    @serverutil.describe(
        appeal_id="Insert the appeal ID shown from the member's appeal message"
    )
    async def approve(self, ctx: Interaction, appeal_id: int):
        await ctx.response.defer()

        if ctx.channel.id == 951783773006073906:
            appeal_data = Appeal(appeal_id)
            check = appeal_data.check_appeal()

            if check == None:
                await ctx.followup.send(f"Invalid appeal ID")
            else:
                member_id = check[0]
                warn_id = check[3]
                member = await self.bot.fetch_user(member_id)

                appeal_data.remove_warn(member_id)

                try:
                    await member.send(
                        f"Hello {member.mention},\nUpon looking into your appeal, we have decided to revoke your warn (**Warn ID:** {warn_id}).\nWe apologies for this and promised that we will be more careful when doing ad moderations against you and other members.\nThank you and enjoy your day!"
                    )
                except:
                    pass

                await ctx.followup.send("Warning revoked and message sent to member")
        else:
            channel = await self.bot.fetch_channel(951783773006073906)
            await ctx.followup.send(
                "Please do the command in {}".format(channel.mention), ephemeral=True
            )

    @serverutil.command(description="Deny an appeal")
    @serverutil.checks.has_role(925790259319558157)
    @serverutil.describe(
        appeal_id="Insert the appeal ID shown from the member's appeal message"
    )
    async def deny(self, ctx: Interaction, appeal_id: int, reason: str):
        await ctx.response.defer()

        if ctx.channel.id == 951783773006073906:
            appeal_data = Appeal(appeal_id)
            check = appeal_data.check_appeal()

            if check == None:
                await ctx.followup.send(f"Invalid appeal ID")
            else:
                member = await ctx.guild.fetch_member(check[0])
                try:
                    await member.send(
                        f"Hello {member.mention},\nUpon looking into your appeal, we have regrettably decided not to revoke your warn (**Warn ID** {check[3]}.\nThe warning will stay\nThank you\n\nReason: {reason}"
                    )

                except:
                    pass

                await ctx.followup.send(
                    "Warning not revoked and message sent to member"
                )
        else:
            channel = await self.bot.fetch_channel(951783773006073906)
            await ctx.followup.send(
                "Please do the command in {}".format(channel.mention), ephemeral=True
            )


async def setup(bot: Bot):
    await bot.add_cog(appealcog(bot), guild=Object(hazead))
