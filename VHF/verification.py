from json import loads
from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Message,
    Object,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog, Cog
from assets.buttons import YesNoButtons
from assets.functions import Verification
from datetime import datetime, timedelta


class VerificationCog(GroupCog, name="verification"):
    def __init__(self, bot: Bot):
        self.bot = bot

        self.approve_verification_context = Serverutil.ContextMenu(
            name="Approve Verification", callback=self.approve_verification
        )
        self.bot.tree.add_command(self.deny_verification_context)

        self.deny_verification_context = Serverutil.ContextMenu(
            name="Deny Verification", callback=self.deny_verification
        )
        self.bot.tree.add_command(self.deny_verification_context)

        self.force_verification_context = Serverutil.ContextMenu(
            name="Force Verification", callback=self.force_verification
        )
        self.bot.tree.add_command(self.force_verification_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.approve_verification_context.name,
            type=self.approve_verification_context.type,
        )
        self.bot.tree.remove_command(
            self.deny_verification_context.name,
            type=self.deny_verification_context.type,
        )
        self.bot.tree.remove_command(
            self.force_verification_context.name,
            type=self.force_verification_context.type,
        )

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def approve_verification(self, ctx: Interaction, message: Message):
        await ctx.response.defer(ephemeral=True)
        data = Verification().check(message.author, message.id)
        embed = Embed()
        embed.color = Color.random()
        if data == True:
            await Verification().approve(message.author)
            try:
                embed.description = f"Hi {message.author}\n\nGlad to say that you have been successfully been verified into {ctx.guild.name}! Now you are a trusted member of the server. Thank you for joining"
                embed.set_footer(
                    text="Please remember that verification doens't mean instant NSFW access. It is your choice to view it or not. We won't in any way or form pressure you. If you were forced to verify, you can add your roles through the self-roles channel"
                )
                await message.author.send(embed=embed)
            except:
                pass

            verification_log = await self.bot.fetch_channel(991655158930997358)
            verification_log_e = Embed()
            verification_log_e.title = "Verification Log (Successful)"
            verification_log_e.add_field(
                name="Member", value=message.author, inline=False
            )
            verification_log_e.add_field(
                name="ID", value=message.author.id, inline=False
            )
            verification_log_e.add_field(
                name="Verified by", value=ctx.user, inline=False
            )
            verification_log_e.add_field(
                name="Verifier ID", value=ctx.user.id, inline=False
            )
            verification_log_e.add_field(
                name="Date and Time",
                value=f"<t:{round(datetime.now().timestamp())}:F>",
                inline=False,
            )
            embed.description = f"{message.author} has successfully been verified! This message will delete soon"
            await ctx.followup.send(embed=embed)
            await verification_log.send(embed=verification_log_e)
            await message.delete(delay=5)
            return
        embed.description = "This member hasn't request to verify yet..."
        embed.color = Color.red()
        await ctx.followup.send(embed=embed)

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def deny_verification(self, ctx: Interaction, message: Message):
        await ctx.response.defer()
        data = Verification().check(message.author, message.id)
        embed = Embed()
        embed.color = Color.random()
        if data == True:
            await Verification().deny(message.author)
            try:
                embed.description = f"Hi {message.author}\n\nWe regret to say that verification has failed but don't worry, you still have another chance to verify unless you were forced to verify which would mean an immediate ban.\n\nThank you"
                embed.set_footer(
                    text="Please remember that verification doens't mean instant NSFW access. It is your choice to view it or not. We won't in any way or form pressure you"
                )
                await message.author.send(embed=embed)
            except:
                pass

            verification_log = await self.bot.fetch_channel(991655158930997358)
            verification_log_e = Embed()
            verification_log_e.title = "Verification Log (Failed)"
            verification_log_e.add_field(
                name="Member", value=message.author, inline=False
            )
            verification_log_e.add_field(
                name="ID", value=message.author.id, inline=False
            )
            verification_log_e.add_field(name="Denied by", value=ctx.user, inline=False)
            verification_log_e.add_field(
                name="Verifier ID", value=ctx.user.id, inline=False
            )
            verification_log_e.add_field(
                name="Date and Time",
                value=f"<t:{round(datetime.now().timestamp())}:F>",
                inline=False,
            )
            embed.description = f"{message.author} has ussuccessfully been verified! This message will delete soon"
            await ctx.followup.send(embed=embed)
            await verification_log.send(embed=verification_log_e)
            await message.delete(delay=5)
            return
        embed.description = "This member hasn't request to verify yet..."
        embed.color = Color.red()
        await ctx.followup.send(embed=embed)

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def force_verification(self, ctx: Interaction, member: Member):
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
        embed.color = Color.red()
        data = Verification().check(ctx.user)
        if data == True:
            embed.description = f"{member} already requested an ID verification"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return

        if data == False:
            embed.description = f"{member} was already verified..."
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return

        await Verification().force(member)
        verify_here = await member.guild.fetch_channel(1059903781552267294)

        embed.description = """
You have been forced to do verification due to one on the following reasons:

1. You are suspected to be underage
2. You were joking about your age
3. You might be impersonating someone
4. You may be a selfbot or userbot

Due to this, **all** your roles have been removed and you have recieved the <@&974760534102650950> role, making the entire server unviewable to you.
"""
        embed.add_field(
            name="How to start verification?",
            value=f"Type `/verification start` in {verify_here.jump_url}. Make sure your DMs are temporary opened for this process",
            inline=False,
        )
        embed.add_field(
            name="What happens if I don't verify?",
            value="We do not recommend that. You have until 48 hours to **successfully** verify or else you might face an immediate ban! This only applies to people who are forced to verify",
            inline=False,
        )
        embed.add_field(
            name="What happens after verification?",
            value="The <@&974760534102650950> role will be removed and you will get <@&974760599487647815> and <@&974760640742825984> roles. You have to manually get your roles back by reacting in https://ptb.discord.com/channels/974028573893595146/976081451709775902 and/or https://ptb.discord.com/channels/974028573893595146/1115725010649235608",
            inline=False,
        )

        try:
            await member.send(embed=embed)
        except:
            await verify_here.send(content=member.mention, embed=embed)
        verification_log = await self.bot.fetch_channel(991655158930997358)
        verification_log_e = Embed()
        verification_log_e.title = "Notice of Force Verification"
        verification_log_e.add_field(
                name="Member", value=member, inline=False
            )
        verification_log_e.add_field(
                name="ID", value=member.id, inline=False
            )
        verification_log_e.add_field(name="Notice by", value=ctx.user, inline=False)
        verification_log_e.add_field(
                name="Verifier ID", value=ctx.user.id, inline=False
            )
        verification_log_e.add_field(
                name="Ban availability",
                value=f"<t:{round((datetime.now() + timedelta(hours=48)).timestamp())}:R>",
                inline=False,
            )
        embed.description = f"Forced Verification notice sent to {member}"
        await ctx.followup.send(embed=embed)
        await verification_log.send(embed=verification_log_e)
        
        await ctx.followup.send(embed=embed)

    @Serverutil.command(name="start", description="Start the verification process")
    async def start(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
        data = Verification().check(ctx.user)
        if data == True:
            embed.description = "You have already requested an ID verification"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return

        if data == False:
            embed.description = "You are already verified..."
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return

        try:
            with open("verification_process.json", "r") as f:
                json_data = loads("".join(f.readlines()))
            dmmsg: Message = await ctx.user.send(
                embed=Embed.from_dict(json_data["embeds"][0])
            )
            await ctx.followup.send(
                embed=Embed(
                    description=f"Go to {dmmsg.jump_url} to start the verification process"
                )
            )
            view = YesNoButtons()
            embed.description = "Have you read the steps and have met the requirements? If not, please do so."
            embed.set_footer(
                text="Please remember that the buttons have a timeout of 10 minutes if there was no interaction"
            )
            await ctx.user.send(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await ctx.edit_original_response(view=None)
                new_requests = []

                def check(m: Message):
                    return m.author == ctx.user and m.attachments

                for i in json_data["steps"]:
                    embed.description = i
                    try:
                        msg: Message = await self.bot.wait_for(
                            "message", check=check, timeout=600
                        )
                        image_url = [
                            x.url
                            for x in msg.attachments
                            if x.url.endswith("jpg", "png", "jpeg")
                        ][0]
                        await ctx.edit_original_response(embed=embed)
                        new_requests.append[image_url]

                    except:
                        embed.description = (
                            "Invalid image format sent. Please restart the verification"
                        )
                        await ctx.edit_original_response(embed=embed)
                        break

                embed.description = "Your verification request has been sent to authorised staff. Please make sure the images you have sent are not deleted as it will be unviewable from our side. You will be able to delete them once we have sent an outcome.\n\nThank you"

                await ctx.edit_original_response(embed=embed)
                verification_channel = await self.bot.fetch_channel(1055487338500857946)
                images = "\n".join(new_requests)

                request = (
                    f"New request from {ctx.user} `{ctx.user.id}`\nImages: {images}"
                )
                m = await verification_channel.send(request)
                await Verification().add_request(ctx.user, m)

        except:
            embed.description = (
                "Please have your DMs temporary opened to start the verification"
            )
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(VerificationCog(bot), guild=Object(974028573893595146))
