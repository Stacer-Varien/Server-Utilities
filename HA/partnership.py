import os
from nextcord import *
from nextcord import slash_command as slash
from nextcord.ext.application_checks import *
from nextcord.ext.commands import Cog, Bot
from assets.functions import check_partnership

#ha
partner_manager = 925790259319558155
admins = 925790259319558157
owner = 925790259319558159

#orleans
management = 762318708596015114



class partner(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash(description='Main Partner Command', guild_ids=[925790259160166460, 740584420645535775])
    async def partner(self, ctx: Interaction):
        pass

    @partner.subcommand(description='Parter with Orleans')
    async def apply(self, ctx: Interaction):
        await ctx.response.defer()
        dm_link = await ctx.user.send(
            "Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite.")
        await ctx.followup.send(f"Please go to your [DMs]({dm_link.jump_url}) to proceed with the partnership")

        def check(m: Message):
            return m.author == ctx.user and m.content

        try:
            ad: Message = await self.bot.wait_for('message', check=check, timeout=180)

            if ctx.guild.id == 740584420645535775:
                with open("HA/orleans.txt") as f:
                    content = "".join(f.readlines())
            
            elif ctx.guild.id == 925790259160166460:
                with open("HA/hazeads.txt") as f:
                    content = "".join(f.readlines())

            await ctx.user.send(content)
            await ctx.user.send(
                "We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot with date and time showing as proof. This is just to avoid partnership scams")

            try:
                def check_image(m: Message):
                    return m.author == ctx.user and m.attachments

                proof:Message = await self.bot.wait_for('message', check=check_image, timeout=180)

                image_urls = [x.url for x in proof.attachments]
                images = "\n".join(image_urls)

                if ctx.guild.id == 740584420645535775:
                    with open("partnerships/orleans/{}.txt".format(ctx.user.id), 'w') as f:
                        f.write(ad.content)
                    partnerchannel = self.bot.get_channel(1051048278181031988)
                    
                elif ctx.guild.id == 925790259160166460:
                    with open("partnerships/hazeads/{}.txt".format(ctx.user.id), 'w') as f:
                        f.write(ad.content)
                    partnerchannel = self.bot.get_channel(981877384192094279)

                await ctx.user.send(
                    "Partnership is now complete. Please wait for a response from us that your partnership request is accepted or denied")

                await partnerchannel.send("```{}```".format(ad.content))

                request = Embed(title="Partnership for Orleans",
                                description="To approve or deny the partnership, use `/partner approve MEMBER` or `/partner deny MEMBER REASON`",
                                color=Color.blue())
                request.set_footer(
                    text=f"Partnership request by {ctx.user}\nPartnership ID: {ctx.user.id}")

                await partnerchannel.send(
                    f"Proof they have posted our ad : {images}", embed=request)
            except TimeoutError:
                await ctx.user.send("You have ran out of time. Please try again later")
        except TimeoutError:
            await ctx.user.send("You have ran out of time. Please try again later")

    @partner.subcommand(description='Approve a partnership')
    @has_any_role(partner_manager, admins, owner, management)
    async def approve(self, ctx: Interaction, member: Member = SlashOption(required=True)):
        await ctx.response.defer()
        if ctx.guild.id == 740584420645535775:
            if check_partnership(ctx.guild.id, ctx.user.id) == True:
                partner_channnel = await ctx.guild.fetch_channel(1040380792406298645)
                partner_role = ctx.guild.get_role(1051047558224543844)
                with open("partnerships/orleans/{}.txt".format(member.id), 'r') as f:
                    content = "".join(f.readlines())
                os.remove("partnerships/orleans/{}.txt".format(member.id))
        elif ctx.guild.id == 925790259160166460:
            if check_partnership(ctx.guild.id, ctx.user.id) == True:
                partner_channnel = await ctx.guild.fetch_channel(1040380792406298645)
                partner_role = ctx.guild.get_role(950354444669841428)
                with open("partnerships/hazeads/{}.txt".format(member.id), 'r') as f:
                    content = "".join(f.readlines())
                os.remove("partnerships/hazeads/{}.txt".format(member.id))
        
        if partner_role in member.roles:
            pass
        else:
            await member.add_roles(partner_role, reason="New Partner")
        await ctx.followup.send("Partnership approved and given role")
        await partner_channnel.send(content=content)

    @partner.subcommand(description='Deny a partnership')
    @has_any_role(partner_manager, admins, owner)
    async def deny(self, ctx: Interaction, member: Member = SlashOption(required=True),
                   reason=SlashOption(required=True)):
        if ctx.guild.id == 740584420645535775:
            if check_partnership(ctx.guild.id, ctx.user.id) == True:
                os.remove("partnerships/orleans/{}.txt".format(member.id))
        elif ctx.guild.id == 925790259160166460:
            if check_partnership(ctx.guild.id, ctx.user.id) == True:
                os.remove("partnerships/orleans/{}.txt".format(member.id))
        try:
            await member.send(
                f"Your partnership request was denied because:\n{reason}")
            await ctx.followup.send("Partnership denied and reason sent")
        except Forbidden:
            await ctx.followup.send("Partnership denied")

def setup(bot: Bot):
    bot.add_cog(partner(bot))
