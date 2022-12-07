from asyncio import TimeoutError
from nextcord import slash_command as slash
from nextcord import Interaction, Embed, SlashOption
from nextcord.ext.commands import Cog, Bot
from config import db, hazead
from random import *
from datetime import *
from nextcord import *


class appealcog(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @slash(description="Appeal your warn", guild_ids=[hazead])
    async def appeal(self, ctx: Interaction, warn_id):
        await ctx.response.defer()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM warnDATA WHERE user_id = ? AND warn_id = ?", (ctx.user.id, warn_id,))
        record = cur.fetchone()

        if record == None:
            await ctx.followup.send(f"Invalid warn ID")

        else:
            cur.execute(
            f"SELECT warn_id FROM warnDATA WHERE user_id = {ctx.user.id}")
            
            appeal_log = ctx.guild.get_channel(951783773006073906)

            try:
                aprocess=await ctx.send(f"Please make sure your DMs are opened to start the appealing process", delete_after=5.0)
                

                await ctx.user.send("Please tell us why we should revoke your warn. Please use links instead of images and vidoes if needed.\nYou have 3 minutes to tell")
                await aprocess.delete()

                def check(m: Message):
                    attachments = bool(m.attachments)
                    content = bool(m.content)
                    if attachments and content == True:
                        return m.author == ctx.user and m.content and m.attachments
                    elif content == True:
                        return m.author == ctx.user and m.content
                    elif attachments == True:
                        return m.author == ctx.user and m.attachments
                    elif attachments == True and content == '':
                        return m.author == ctx.user and m.attachments

                try:
                    msg:Message = await self.bot.wait_for('message', check=check, timeout=180)
                
                    await ctx.user.send("Thank you for appealing for your warn. The appropriate staff member will review it and will send updates if any action is needed\nPlease do not rush us or your appeal will be denied.")
                
                    reason = record[2]
                    moderator = await self.bot.fetch_user(record[1])
                    appeal_id=record[4]

                    appeal = Embed(title=f"{ctx.user}'s appeal")
                    appeal.add_field(name="Warn ID", value=warn_id, inline=True)
                    appeal.add_field(name="Appeal ID", value=appeal_id, inline=True)
                    appeal.add_field(name="Warn reason", value=f"{reason}\nWarned by: {moderator}")
                    appeal.set_footer(text="To approve the appeal, use `/verdict accept appeal_id`. To deny the appeal, use `/verdict deny appeal_id`")
                    if msg.content != '':
                        msg=msg.content
                    else:
                        pass
                    try:
                        image_urls = [x.url for x in msg.attachments]
                        images = "\n".join(image_urls)
                        await appeal_log.send("{}\n{}".format(msg, images), embed=appeal)
                    except:
                        await appeal_log.send(msg, embed=appeal)
                except TimeoutError:
                    await ctx.user.send("You have ran out of time. Please try again.")
            except:
                dmopen=await ctx.send("Please open your DMs to start the appeal process", delete_after=5.0)

            


    @slash(description="Approve or deny an appeal", guild_ids=[hazead])
    async def verdict(self, ctx: Interaction, appeal_id, verdict=SlashOption(choices=["Approve", "Deny"])):
        await ctx.response.defer()
        if ctx.permissions.administrator is True:
            cur = db.cursor()
            cur.execute(
                f"SELECT * FROM warnData WHERE appeal_id = {appeal_id}")
            record = cur.fetchone()
            member_id=record[0]
            warn_id=record[3]
            member= await self.bot.fetch_user(member_id)

            if record == None:
                await ctx.followup.send(f"Invalid appeal ID")
            
            else:
                if verdict == "Approve":
                    cur.execute(
                        f"DELETE FROM warnData WHERE appeal_id = {appeal_id}")

                    cur.execute(f"UPDATE warnDATA_v2 SET warn_point = warn_point - 1 where user_id = {member_id}")
                    db.commit()

                    try:
                        await member.send(f"Hello {member.mention},\nUpon looking into your appeal, we have decided to revoke your warn (**Warn ID:** {warn_id}).\nWe apologies for this and promised that we will be more careful when doing ad moderations against you and other members.\nThank you and enjoy your day!")
                    except:
                        pass

                    await ctx.followup.send("Warning revoked and message sent to member")

                elif verdict == "Deny":
                    try:
                        
                        await ctx.followup.send("Do you have anything to say why it won't be revoked? Type 'Y' for yes and 'N' for no.")

                        def check(m):
                            return m.author == ctx.user and m.content

                        confirm = await self.bot.wait_for('message', check=check, timeout=60)

                        if 'Y' in confirm.content:
                            await ctx.followup.send("Please type what you have to say why it won't be revoked.\nYou have 60 seconds")
                            
                            note = await self.bot.wait_for('message', check=check, timeout=60)

                            await member.send(f"Hello {member.mention},\nUpon looking into your appeal, we have regrettably decided not to revoke your warn (**Warn ID** {warn_id}.\nThe warning will stay\nThank you\n\nNote from us: {note.content}")

                        elif 'N' in confirm.content:
                            await member.send(f"Hello {member.mention},\nUpon looking into your appeal, we have regrettably decided not to revoke your warn (**Warn ID** {warn_id}.\nThe warning will stay\nThank you")

                    except:
                        pass

                    await ctx.followup.send("Warning not revoked and message sent to member")
                

def setup(bot):
    bot.add_cog(appealcog(bot))
