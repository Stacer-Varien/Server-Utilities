from nextcord import *
from nextcord.ext.commands import Bot
from assets.functions import get_appeal_id
from config import db


class Strike_Appeal(ui.Modal):
    def __init__(self, bot:Bot, strike_id, department):
        self.bot = bot
        self.strike_id = strike_id
        self.department = department
        super().__init__(
            "Strike Appeal Form")

        self.strike_appeal = ui.TextInput(label="Reason of appeal", min_length=4, max_length=1024,
                                          required=True, placeholder="Enter your reason here",
                                          style=TextInputStyle.paragraph)
        self.add_item(self.strike_appeal)

    async def callback(self, ctx: Interaction) -> None:
        appeal_id = get_appeal_id(self.strike_id, self.department)

        embed = Embed(title="New Strike Appeal")
        embed.add_field(name="Staff member", value="{} | {}".format(ctx.user, ctx.user.id), inline=False)
        embed.add_field(name="Department", value=self.department, inline=True)
        embed.add_field(name="Reason of Appeal", value=self.strike_appeal.value, inline=False)
        embed.add_field(name="Strike Appeal ID", value=appeal_id, inline=False)
        embed.set_footer(
            text="To accept or deny the appeal, use `/strike verdict STRIKE_APPEAL_ID accept` or `/strike verdict STRIKE_APPEAL_ID deny`")
        db.commit()
        channel = self.bot.get_channel(1004744695085285457)

        return await channel.send(embed=embed)


class Start_Appeal(ui.View):
    def __init__(self, bot:Bot, strike_id, department):
        self.bot = bot
        self.strike_id = strike_id
        self.department = department
        super().__init__(timeout=600)
        self.value = None

    @ui.button(label="Continue", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = True
        await ctx.response.send_modal(Strike_Appeal(self.bot, self.strike_id, self.department))
        self.stop()
