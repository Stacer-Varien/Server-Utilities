from json import loads
from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Message,
    app_commands as Serverutil,
)
from discord.ext.commands import Bot, GroupCog, Cog
from assets.buttons import YesNoButtons


class VerificationCog(GroupCog, name="verification"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.approve_verification_context = Serverutil.ContextMenu(
            name="Approve Verification", callback=self.approve_verification
        )
        self.bot.tree.add_command(self.approve_verification_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.approve_verification_context.name,
            type=self.approve_verification_context.type,
        )

    @Serverutil.checks.has_any_role(977127630518226944, 1003586650498146344)
    async def approve_verification(self, ctx:Interaction, member:Member):
        ...

    @Serverutil.command(name="start", description="Start verifying in VHF")
    async def start(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
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

                embed.description = "Your verification request has been sent to us including authorised staff. Please make sure the images you have sent are not deleted as it will be unviewable from our side. You will be able to delete them once we have sent an outcome.\n\nThank you"

                await ctx.edit_original_response(embed=embed)
                verification_channel = await self.bot.fetch_channel(1055487338500857946)
                images = "\n".join(new_requests)
                request = (
                    f"New request from {ctx.user} `{ctx.user.id}`\nImages: {images}"
                )
                await verification_channel.send(request)

        except:
            embed.description = (
                "Please have your DMs temporary opened to start the verification"
            )
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(VerificationCog(bot))
