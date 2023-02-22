from datetime import timedelta, datetime
import os
from discord import AllowedMentions, Embed, Interaction, Color, Message, Object
from discord import app_commands as Serverutil
from discord.ext.commands import GroupCog, Bot, ExtensionNotLoaded
import requests
from config import lss, hazead, loa, orleans
from humanfriendly import parse_timespan
from assets.functions import Plans, convert_loop_time
from assets.ad_insert_modal import Ad_Insert
from os import path
from assets.autoad_manage import AutoadManage


class autoadcog(GroupCog, name='automod'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Serverutil.command(description="Create an autoad and starts it")
    @Serverutil.checks.has_any_role(841671779394781225, 1077172702743371787)
    @Serverutil.describe(
        buyer_id="What is the buyer's user ID?",
        name="What will you name the autoad?",
        looptime="How long per interval will the ad be autoposted",
        ends=
        "How long will the autoad last? (Example: 1m (1 minute), 3w (3 weeks), 2y (2 years))",
        channels=
        "Which channels will the ads be posted (use channel IDs and leave a space after each ID)"
    )
    async def create(self, ctx: Interaction, buyer_id: str, name: str,
                     looptime: str, ends: str, channels: str):
        ad_path = f"/autopost/{name}.py"
        check = path.exists(ad_path)
        embed = Embed()
        if check == True:
            embed.description = f"{name} autoad already exists. If it is for a seperate server, please name it as something else"
            embed.color = Color.red()
        else:
            timed = parse_timespan(looptime)
            looping = convert_loop_time(timed)

            ending = datetime.now() + timedelta(seconds=parse_timespan(ends))

        await ctx.response.send_modal(
            Ad_Insert(self.bot, int(buyer_id), name, looping,
                      round(ending.timestamp()), channels))

    @Serverutil.command(description="Manages an autoad")
    @Serverutil.checks.has_any_role(841671779394781225, 1077172702743371787)
    @Serverutil.describe(autoad_name="What is the name of the autoad")
    async def manage(self, ctx: Interaction, autoad_name: str):
        await ctx.response.defer()
        ad_path = f"/autopost/{autoad_name}.py"
        check = os.path.exists(ad_path)

        if check == True:
            view = AutoadManage()
            await ctx.followup.send(view=view)
            await view.wait()

            if view.value == 'start':
                await self.bot.load_extension(f"autopost.{autoad_name}")
                await ctx.edit_original_response(
                    content=f"Autoad {autoad_name} has started", view=None)
            elif view.value == 'stop':
                await self.bot.unload_extension(f"autopost.{autoad_name}")
                await ctx.edit_original_response(
                    content=f"Autoad {autoad_name} has stopped", view=None)
            elif view.value == 'cancel':
                try:
                    await self.bot.unload_extension(f"autopost.{autoad_name}")
                except:
                    pass
                os.remove(f"/autopost/{autoad_name}.py")
                await ctx.edit_original_response(
                    content=f"Autoad {autoad_name} has been removed",
                    view=None)
            elif view.value == 'change_ad':
                await ctx.edit_original_response(
                    "Provide the ad in a text file and send it back. You have 6 minutes"
                )

                def check(m: Message):
                    return m.author == ctx.user and m.attachments

                try:
                    msg: Message = await self.bot.wait_for('message',
                                                           check=check,
                                                           timeout=600)

                    attachment = msg.attachments[0].url

                    ad = requests.get(attachment).content
                    os.remove(f"/autopost/{autoad_name}.text")

                    with open(f"/autopost/{autoad_name}.txt", 'wb') as f:
                        f.write(ad)

                    await ctx.edit_original_response(
                        f"Ad for {autoad_name} has been changed")
                except TimeoutError:
                    await ctx.edit_original_response("Timeout")
        else:
            await ctx.followup.send(
                "No Autoad has that name. Please try and check if you have put the correct autoad"
            )


async def setup(bot: Bot):
    await bot.add_cog(autoadcog(bot))