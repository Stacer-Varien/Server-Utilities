from datetime import timedelta, datetime
from discord import Embed, Interaction, Color, Object
from discord import app_commands as Serverutil
from discord.ext.commands import GroupCog, Bot, Context, check
from config import lss, hazead, loa, orleans
from humanfriendly import parse_timespan, format_timespan
from assets.functions import convert_loop_time
from assets.ad_insert_modal import Ad_Insert
from os import path


class autoadcog(GroupCog, name='automod'):

    def __init__(self, bot: Bot):
        self.bot = bot

    def is_autoader():
        def predicate(ctx:Interaction):
            with open('assets.autoaders.txt', 'r') as f:
                content=f.readlines()
            if ctx.user.id in content:
                return ctx.user
        return Serverutil.check(predicate)


    @Serverutil.command(description="Create an autoad and starts it")
    @is_autoader()
    @Serverutil.describe(
        buyer_id="What is the buyer's user ID?",
        name="What will you name the autoad?",
        looptime="How long per interval will the ad be autoposted",
        ends=
        "How long will the autoad last? (Example: 1m (1 minute), 3w (3 weeks), 2y (2 years))",
        channels=
        "Which channels will the ads be posted (use channel IDs and leave a space after each ID)"
    )
    async def create(self, ctx: Interaction, buyer_id:str, name: str, looptime: str,
                     ends: str, channels: str):
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

        await ctx.response.send_modal(Ad_Insert(self.bot, int(buyer_id), name, looping, round(ending.timestamp()), channels))

    @Serverutil.command(description="Manages an autoad")
    
