from asyncio import TimeoutError
from discord import Color, Member, app_commands as serverutil
from discord import Interaction, Embed, Object
from discord.ext.commands import GroupCog, Bot
from assets.functions import LOAWarn, Warn, Appeal
from config import hazead, loa
from discord import Message


class appealcog(GroupCog, name="appeal"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def HA_appeal(self, ctx: Interaction, warn_id: int):
        check_warn = Warn(ctx.user, warn_id).check()
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

                    appeal = Embed(title=f"{ctx.user}'s appeal")
                    appeal.add_field(name="Warn ID", value=warn_id, inline=True)
                    appeal.add_field(
                        name="Warn reason",
                        value=f"{reason}\nWarned by: {moderator}",
                        inline=False,
                    )
                    appeal.set_footer(
                        text="To approve the appeal, use `/appeal accept warn_id``"
                    )

                    try:
                        image_urls = [x.url for x in msg.attachments]
                        images = "\n".join(image_urls)
                        await appeal_log.send(
                            "{}\n{}".format(msg.content, images), embed=appeal
                        )
                    except:
                        await appeal_log.send(msg.content, embed=appeal)
                except:
                    await ctx.user.send("You have ran out of time. Please try again.")
            except:
                await ctx.followup.send(
                    "Please open your DMs to start the appeal process", ephemeral=True
                )

    async def LOA_appeal(self, ctx: Interaction, warn_id: int):
        warn_data = LOAWarn(user=ctx.user, warn_id=warn_id).check()

        if warn_data == None:
            await ctx.followup.send(
                "You do not have warning corresponding with this warn ID",
                ephemeral=True,
            )
        else:
            try:
                msg = await ctx.user.send(
                    "Please explain why your adwarn should be revoked? If applicable, please send media content to support your appeal. Please know that sending your ad ONLY would be considered as an instant DM advertising and your appeal will be denied.\n\nYou have 5 minutes to appeal"
                )

                await ctx.followup.send(
                    f"[Click here]({msg.jump_url}) to process your appeal"
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
                    appeal_log = await self.bot.fetch_channel(1107611200843427931)
                    msg: Message = await self.bot.wait_for(
                        "message", check=check, timeout=600
                    )

                    await ctx.user.send(
                        "Thank you for appealing for your warn. The appropriate staff member will review it and will notify you if your appeal was approved.\nIf your appeal was not approved after a week, it means that it was denied.\n\nPlease do not rush us or your appeal will be denied almost immediately."
                    )

                    embed = Embed(description="New Warn Appeal", color=Color.random())
                    embed.add_field(
                        name="Person who is appealling it",
                        value=f"{ctx.user} | `{ctx.user.id}`",
                        inline=False,
                    )
                    embed.add_field(name="Warn ID", value=warn_id, inline=False)
                    embed.add_field(
                        name="Reason of warn", value=warn_data[1], inline=False
                    )
                    embed.set_footer(
                        text="To approve this appeal, use `/appeal approve WARN_ID`"
                    )

                    try:
                        image_urls = [x.url for x in msg.attachments]
                        images = "\n".join(image_urls)
                        await appeal_log.send(
                            "{}\n{}".format(msg.content, images), embed=embed
                        )
                    except:
                        await appeal_log.send(msg.content, embed=embed)

                    await ctx.user.send(
                        "Your appeal has been submitted. Please wait patiently for the appropriate staff to decide.\nRushing us could increas your chance of your appeal being denied"
                    )
                except TimeoutError:
                    await ctx.user.send("Times up! Please try again later")
            except:
                await ctx.followup.send("Please open your DMs to do the appeal process")

    async def approve_HA_appeal(self, ctx: Interaction, member: Member, warn_id: int):
        if ctx.channel.id == 951783773006073906:
            appeal_data = Appeal(member, warn_id)
            check = appeal_data.check()

            if check == None:
                await ctx.followup.send(f"Invalid warn ID")
            else:
                member_id:int = check[0]
                warn_id:int = check[3]
                member = await self.bot.fetch_user(member_id)

                appeal_data.remove()

                try:
                    await member.send(
                        f"Hello {member.mention},\nUpon looking into your appeal, we have decided to revoke your warn (**Warn ID:** {warn_id}).\nWe apologies for this and promised that we will be more careful when doing ad moderations against you and other members.\nThank you and enjoy your day!"
                    )
                except:
                    pass

                await ctx.followup.send("Warning revoked and message sent to member")
        else:
            ch = await self.bot.fetch_channel(951783773006073906)
            await ctx.followup.send(
                "Please do the command in {}".format(ch.mention), ephemeral=True
            )

    async def approve_LOA_appeal(self, ctx: Interaction, member: Member, warn_id: int):
        warn_data = LOAWarn(user=member, warn_id=warn_id)

        if warn_data.check() == None:
            await ctx.followup.send(
                "This user has not been warned or incorrect warn ID",
                ephemeral=True,
            )
        else:
            modchannel1 = await ctx.guild.fetch_channel(954594959074418738)
            if ctx.channel.id == 954594959074418738 or ctx.channel.id == 1112136237034246205:
                warn_data.remove()
                modchannel = await ctx.guild.fetch_channel(745107170827305080)
                appealed = Embed(
                    description=f"Your appeal has been approved. You now have {warn_data.get_points()} adwarns",
                    color=Color.random(),
                )
                await ctx.followup.send("Appeal approved")
                await modchannel.send(member.mention, embed=appealed)
            else:
                await ctx.followup.send(
                    "Please do this command in {}".format(modchannel1.mention)
                )

    @serverutil.command(description="Apply for an adwarn appeal")
    @serverutil.describe(warn_id="Insert the warn ID that you wish to appeal your warn")
    async def apply(self, ctx: Interaction, warn_id: int):
        await ctx.response.defer()
        if ctx.guild.id == 925790259160166460:
            await self.HA_appeal(ctx, warn_id)
        elif ctx.guild.id == 925790259160166460:
            await self.LOA_appeal(ctx, warn_id)

    @serverutil.command(description="Approve an appeal")
    @serverutil.checks.has_any_role(
        925790259319558159,
        925790259319558158,
        925790259319558157,
        1011971782426767390,
        925790259319558154,
        889019375988916264,
        749608853376598116,
        919410986249756673,
        947109389855248504,
        849778145087062046
    )
    @serverutil.describe(warn_id="Insert the warn_id ID shown from the member's appeal")
    async def approve(self, ctx: Interaction, member: Member, warn_id: int):
        await ctx.response.defer()
        if ctx.guild.id == 925790259160166460:
            await self.approve_HA_appeal(ctx, member, warn_id)
        elif ctx.guild.id == 704888699590279221:
            await self.approve_LOA_appeal(ctx, member, warn_id)

async def setup(bot: Bot):
    await bot.add_cog(appealcog(bot), guilds=[Object(hazead), Object(loa)])
