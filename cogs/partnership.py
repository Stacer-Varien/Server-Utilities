from nextcord.ext.commands import Cog
from nextcord import *
from datetime import *
from nextcord import slash_command as slash
from config import HA_WEBHOOK, HAZE_WEBHOOK, db
from nextcord.ext.application_checks import *

partner_manager = 925790259319558155
admins = 925790259319558157
owner = 925790259319558159
                  

class partner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(description='Main Partner Command')
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
            await ctx.user.send("We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot as proof in a media link. This is just to avoid partnership scams\n\nIf you don't know how to do it, send the proof as it is, right click on it and select copy link and send the link here.")

            try:
                proof = await self.bot.wait_for('message', check=check, timeout=180)

                await ctx.user.send("Partnership is now complete. Please wait for a response from us that your partnership request is accepted or denied")


                partnerchannel = self.bot.get_channel(928971022315708416)
                msg = await partnerchannel.send(ad.content)

                request = Embed(title="Partnership for HAZE",
                    description="To approve or deny the partnership, use `/partner approve ID` or `/partner deny ID REASON`", color=Color.blue())
                request.set_footer(
                    text=f"Partner ID: {msg.id} requested by {ctx.user}")
                
                await partnerchannel.send(
                    f"Proof they have posted our ad : {proof.content}", embed=request)
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
            await ctx.user.send("We have given you our ad. Now, you have 3 minutes to post our ad to your server and send a FULL screenshot as proof in a media link. This is just to avoid partnership scams\n\nIf you don't know how to do it, send the proof as it is, right click on it and select copy link and send the link here.")

            try:
                proof = await self.bot.wait_for('message', check=check, timeout=180)

                await ctx.user.send("Partnership is now complete. Please wait for a response from us that your partnership request is accepted or denied")

                partnerchannel = self.bot.get_channel(981877384192094279)
                msg = await partnerchannel.send(ad.content)

                db.execute("INSERT OR IGNORE INTO partnerData (msg_id, user_id) VALUES (?,?,?)",(msg.id, ctx.user.id))
                db.commit()

                request = Embed(title=f"Partnership for HAZE Advertising from {ctx.user}",
                    description="To approve or deny the partnership, use `/partner approve ID APPLIER` or `/partner deny ID REASON`", color=Color.blue())
                request.set_footer(
                    text=f"Partner ID: {msg.id} requested by Applier: {ctx.user.id}")
                
                await partnerchannel.send(
                    f"Proof they have posted our ad : {proof.content}", embed=request)
            except TimeoutError:
                await ctx.user.send("You have ran out of time. Please try again later")
        except TimeoutError:
            await ctx.user.send("You have ran out of time. Please try again later")

    @partner.subcommand(description='Approve a partnership')
    @has_any_role(partner_manager, admins, owner)
    async def approve(self, ctx: Interaction, server=SlashOption(choices=['HAZE', 'HAZE Advertising'], required=True),  partner_id=SlashOption(required=True)):
        await ctx.response.defer()
        partnerchannel = self.bot.get_channel(981877384192094279)
        partnerapp=await partnerchannel.fetch_message(partner_id)
        if server == 'HAZE':
            webhook = SyncWebhook.from_url(HAZE_WEBHOOK)
            webhook.send(embed=partnerapp.content)
            await ctx.followup.send("Partnership approved")
        elif server == 'HAZE Advertising':
            webhook = SyncWebhook.from_url(HA_WEBHOOK)
            webhook.send(embed=partnerapp.content)
            partner_role = ctx.guild.get_role(950354444669841428)
            user_id=db.execute(f"SELECT user_id FROM parterData WHERE msg_id = {partner_id}").fetchone()[0]
            user=await ctx.guild.fetch_member(user_id)
            await user.add_roles(partner_role)
            await ctx.followup.send("Partnership approved and given role")

    @partner.subcommand(description='Deny a partnership')
    async def deny(self, ctx: Interaction, partner_id=SlashOption(required=True), reason=SlashOption(required=True)):
        await ctx.response.defer()
        partnerchannel = self.bot.get_channel(981877384192094279)
        partnerapp=await partnerchannel.fetch_message(partner_id)
        await partnerapp.delete()
        user_id=db.execute(f"SELECT user_id FROM parterData WHERE msg_id = {partner_id}").fetchone()[0]
        user=await ctx.guild.fetch_member(user_id)
        try:
            await user.send(f"Your partnership request was denied because:\n{reason}")
            await ctx.followup.send("Partnership denied and reason sent")
        except:
            await ctx.followup.send("Partnership denied")
        


def setup(bot):
    bot.add_cog(partner(bot))
