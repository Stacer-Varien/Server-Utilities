from nextcord.ext.commands import Cog
from nextcord import *
from datetime import *
from nextcord import slash_command as slash
from assets.functions import add_partnership_request, get_partnership_request, remove_partnership_request
from config import HA_WEBHOOK, HAZE_WEBHOOK, db
from nextcord.ext.application_checks import *

partner_manager = 925790259319558155
admins = 925790259319558157
owner = 925790259319558159
                  

class partner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description='Main Partner Command', guild_ids=[925790259160166460])
    async def partner(self, ctx:Interaction):
        pass

    @partner.subcommand(description='Parter with HAZE')
    async def haze(self, ctx: Interaction):
        await ctx.response.defer()
        dm_link = await ctx.user.send("Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite.")
        await ctx.followup.send(f"Please go to your [DMs]({dm_link.jump_url}) to proceed with the partnership")

        def check(m):
            return m.author == ctx.user and m.content

        await ctx.user.send("Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite.")
        try:
            ad = await self.bot.wait_for('message', check=check, timeout=180)

            with open("cogs/haze.txt") as f:
                    content = "".join(f.readlines())

            await ctx.user.send(content)
            await ctx.user.send("We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot as proof. This is just to avoid partnership scams")

            try:
                def check_image(m):
                    return m.author == ctx.user and m.attachments

                proof = await self.bot.wait_for('message', check=check_image, timeout=180)

                image_urls = [x.url for x in msg.attachments]
                image_urls = "\n".join(image_urls)

                add_partnership_request(
                    ctx.user.id, ad.content, proof.content, 740584420645535775)

                await ctx.user.send("Partnership is now complete. Please wait for a response from us that your partnership request is accepted or denied")


                partnerchannel = self.bot.get_channel(981877384192094279)
                msg = await partnerchannel.send("```{}```".format(ad.content))

                request = Embed(title="Partnership for HAZE",
                    description="To approve or deny the partnership, use `/partner approve ID` or `/partner deny ID REASON`", color=Color.blue())
                request.set_footer(
                    text=f"Partner ID: {msg.id} requested by {ctx.user}")
                
                await partnerchannel.send(
                    f"Proof they have posted our ad : {proof}", embed=request)
            except TimeoutError:
                await ctx.user.send("You have ran out of time. Please try again later")
        except TimeoutError:
            await ctx.user.send("You have ran out of time. Please try again later")

    @partner.subcommand(description='Parter with HAZE Advetrising')
    async def haze_advertising(self, ctx: Interaction):
        await ctx.response.defer()
        dm_link = await ctx.user.send("Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite.")
        await ctx.followup.send(f"Please go to your [DMs]({dm_link.jump_url}) to proceed with the partnership")

        def check(m):
            return m.author == ctx.user and m.content

        await ctx.user.send("Please send your ad. Make sure the invite is permanent and is not a vanity URL or custom url, not in codeblock and does not have custom emojis. If not, your partnership will be revoked due to an expired invite.")
        try:
            ad = await self.bot.wait_for('message', check=check, timeout=180)

            with open("cogs/hazead.txt") as f:
                    content = "".join(f.readlines())

            await ctx.user.send(content)
            await ctx.user.send("We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot as proof. This is just to avoid partnership scams.")

            try:
                def check_image(m):
                    return m.author == ctx.user and m.attachments

                proof = await self.bot.wait_for('message', check=check_image, timeout=180)

                image_urls = [x.url for x in msg.attachments]
                image_urls = "\n".join(image_urls)

                partnerchannel = self.bot.get_channel(981877384192094279)
                msg = await partnerchannel.send("```{}```".format(ad.content))

                add_partnership_request(ctx.user.id, ad.content, proof.content, ctx.guild.id)

                request = Embed(title=f"Partnership for HAZE Advertising from {ctx.user}",
                    description="To approve or deny the partnership, use `/partner approve ID APPLIER` or `/partner deny ID REASON`", color=Color.blue())
                request.set_footer(
                    text=f"Partner ID: {msg.id} requested by Applier: {ctx.user.id}")
                
                await partnerchannel.send(
                    f"Proof they have posted our ad : {proof}", embed=request)
            except TimeoutError:
                await ctx.user.send("You have ran out of time. Please try again later")
        except TimeoutError:
            await ctx.user.send("You have ran out of time. Please try again later")

    @partner.subcommand(description='Approve a partnership')
    @has_any_role(partner_manager, admins, owner)
    async def approve(self, ctx: Interaction, member:Member=SlashOption(required=True),server=SlashOption(choices=['HAZE', 'HAZE Advertising'], required=True)):
        await ctx.response.defer()
        if server == "HAZE":
            request = get_partnership_request(member.id, 740584420645535775)

            if request == None:
                await ctx.followup.send("User did not apply for partnership for this server.")
            else:
                webhook = SyncWebhook.from_url(HAZE_WEBHOOK)
                webhook.send(content=request[1])
                await ctx.followup.send("Partnership approved")
                remove_partnership_request(member.id, 740584420645535775)
        elif server == "HAZE Advertising":
            request = get_partnership_request(member.id, ctx.guild.id)

            if request == None:
                await ctx.followup.send("User did not apply for partnership for this server.")
            else:
                webhook = SyncWebhook.from_url(HA_WEBHOOK)
                webhook.send(content=request[1])
                partner_role = ctx.guild.get_role(950354444669841428)
                await member.add_roles(partner_role)
                await ctx.followup.send("Partnership approved and given role")
                remove_partnership_request(member.id, ctx.guild.id)

    @partner.subcommand(description='Deny a partnership')
    @has_any_role(partner_manager, admins, owner)
    async def deny(self, ctx: Interaction, member:Member=SlashOption(required=True), reason=SlashOption(required=True)):
        ids = [740584420645535775, ctx.guild.id]
        for i in ids:
            try:
                remove_partnership_request(member.id, i)
            except:
                pass
        try:
            await member.send(f"Your partnership request was denied because:\n{reason}\n\nPlease note that it is denied in both servers applicable")
            await ctx.followup.send("Partnership denied and reason sent")
        except Forbidden:
            await ctx.followup.send("Partnership denied")
        


def setup(bot):
    bot.add_cog(partner(bot))
