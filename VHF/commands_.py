from nextcord import *
from nextcord import slash_command as slash
from config import *
from nextcord.ext.commands import *
from assets.functions import *

class cmds_(Cog):
    def __init__(self, bot:Bot):
        self.bot=bot

    @slash(description="Main ID verify command", guild_ids=[974028573893595146])
    async def idverify(self, ctx:Interaction):
        ...

    @idverify.subcommand(description="Verify yourself to be a trusted member in VHF")
    async def request(self, ctx:Interaction):
        verify_role = ctx.guild.get_role(974760640742825984)
        if verify_role in ctx.user.roles:
            await ctx.followup.send('You are already verified ( ._.)', ephemeral=True)
        else:
            try:
                msg= await ctx.user.send("Please send the pictures as mentioned in <#974760508240576553>.\nIf you were verified in one of our partnered servers (found in <#1003576509858058290>), send proof that you have an ID verified role in your profile.\n\nYou have 3 minutes to sent everything")
                await ctx.response.defer("Check your [DMs]({})".format(msg.jump_url))

                def check(m: Message):
                    attachments = bool(m.attachments)
                    content = bool(m.content)
                    if attachments and content == True:
                        return m.author == ctx.user and m.content and m.attachments
                    elif attachments == True:
                        return m.author == ctx.user and m.attachments
                try:
                    msg:Message = await self.bot.wait_for('message', check=check, timeout=180)

                    if msg.content == False or None or '':
                        msg.content=None

                    image_urls = [x.url for x in msg.attachments]
                    image_urls = "\n".join(image_urls)

                    verification_channel= await ctx.guild.fetch_channel(1055487338500857946)
                    msgs='{}\n{}'.format(msg.content, image_urls)
                    thread=await verification_channel.create_thread(name=ctx.user, message="Verification Request of {}".format(ctx.user), reason="Verification Request")

                    await thread.send(content=msgs)

                    await ctx.user.send("Thank you for requesting an ID verification. Please wait patiently for a verifier to complete the process.\nRushing us will lower your chances of being verified quickly, not at all or denied")
                except TimeoutError:
                    await ctx.followup.send("You ran out of time ( ._.)", ephemeral=True)  
            except:
                await ctx.followup.send("Your DMs are closed ( ._.)", ephemeral=True)

    @idverify(description="Approve an ID verification request")
    @has_role(1003586650498146344)
    async def approve(self, ctx:Interaction, member:Member):
        await ctx.response.defer()
        verify_role = ctx.guild.get_role(974760640742825984)
        log = ctx.guild.get_channel(991655158930997358)
        if check_verification_request(member.id) == None:
            await ctx.followup.send("{} did not do an ID verification".format(member), ephemeral=True)
        elif verify_role in member.roles:
            await ctx.followup.send("{} was already verified ( ._.)".format(member), ephemeral=True)
        else:
            embed=Embed()
            embed.description="{} has successfully been verified and given the role".format(member)
            embed.color=Color.green()
            
            loge=Embed()
            loge.description="{} | `{}` has been verified by {} | `{}`".format(member, member.id, ctx.user, ctx.user.id)
            loge.color=Color.green()

            await member.add_roles(verify_role, reason="Passed verification")
            try:
                await member.send("Hello, you are now an ID verified member of {}".format(ctx.guild.name))
            except:
                pass

            await ctx.followup.send("{} has been verified".format(member))
            await log.send(embed=embed)

    @idverify(description="Deny an ID verification request")
    @has_role(1003586650498146344)
    async def deny(self, ctx: Interaction, member: Member, reason:str, ban:bool=SlashOption(required=None)):
        await ctx.response.defer()
        verify_role = ctx.guild.get_role(974760640742825984)
        log = ctx.guild.get_channel(991655158930997358)
        if check_verification_request(member.id) == None:
            await ctx.followup.send("{} did not do an ID verification".format(member), ephemeral=True)
        elif verify_role in member.roles:
            await ctx.followup.send("{} was already verified ( ._.)".format(member), ephemeral=True)
        else:
            embed = Embed()
            embed.description = "{} has denied being verified with reason: `{}`".format(member, reason)
            embed.color = Color.red()

            loge = Embed()
            loge.description = "{} | `{}` has been denied verification by {} | `{}`".format(
                member, member.id, ctx.user, ctx.user.id)
            loge.color = Color.red()
            loge.add_field(name="Reason", value=reason, inline=False)

            
            try:
                await member.send("Hello, you verification for {} has been denied because: `{}`".format(ctx.guild.name, reason))
            except:
                pass

            if ban == True:
                await member.ban(reason="Failed verification\n{} | {} / {}".format(reason, ctx.user, ctx.user.id))
            elif ban == False or None:
                pass
            else:
                pass

            await ctx.followup.send("{} has been denied verification".format(member))
            await log.send(embed=embed)

    @slash(description="Make a member untrusted")
    @has_any_role(1003586650498146344, 977127630518226944)
    async def untrust(self, ctx: Interaction, member: Member, reason:str=SlashOption(choices=['Joking about age', 'Suspected of being underage'])):
        await ctx.response.defer()
        untrusted=ctx.guild.get_role(974760534102650950)
        await member.add_roles(untrusted, reason="Untrusted in this server")
        await member.send("You have been marked untrusted in {}. All channels are now unviewable to you unless you verify.\nPlease verify within 48 hours or you will be banned. The instructions are shown in <#974760508240576553>")

        def check(m: Message):
            attachments = bool(m.attachments)
            content = bool(m.content)
            if attachments and content == True:
                return m.author == ctx.user and m.content and m.attachments
            elif attachments == True:
                return m.author == ctx.user and m.attachments
        try:
            msg: Message = await self.bot.wait_for('message', check=check, timeout=172800)

            if msg.content == False or None or '':
                msg.content=None

            image_urls = [x.url for x in msg.attachments]
            image_urls = "\n".join(image_urls)

            verification_channel= await ctx.guild.fetch_channel(1055487338500857946)
            
            msgs='{}\n{}'.format(msg.content, image_urls)
            thread=await verification_channel.create_thread(name=ctx.user, message="Verification Request of {}".format(ctx.user), reason="Verification Request")
                        
            await thread.send(content=msgs)

            await ctx.user.send("Thank you for sending your documents. Please wait patiently for a verifier to complete the process.\nRushing us will lower your chances of being verified quickly, not at all or denied")
        except TimeoutError:
            await member.send('You have been banned from {} because you failed to verify'.format(ctx.guild.name))
            await member.ban(reason="Failed verification\n{} | {} / {}".format(reason, ctx.user, ctx.user.id))

def setup(bot:Bot):
    bot.add_cog(cmds_(bot))
        
