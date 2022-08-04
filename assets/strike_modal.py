from random import randint
from nextcord import *
from config import db

class Strike_Appeal(ui.Modal):
    def __init__(self, bot):
        self.bot=bot
        super().__init__("Strike Appeal\nIf you believe your strike was unfair, please fill in below. Please remember to have proof if necessary")

        self.department = ui.TextInput(label="Which department do you work for?", min_length=2, max_length=50, placeholder="Enter the department here. Remember it has to be the exact were you were striked", required=True)
        self.add_item(self.department)
        self.strike_appeal = ui.TextInput(label="Reason for appeal", min_length=4, max_length=1024,
                                         required=True, placeholder="Enter your reason here", style=TextInputStyle.paragraph)
        self.add_item(self.strike_appeal)

    async def callback(self, ctx: Interaction) -> None:

        strike_id = randint(0,99999)

        db.execute("INSERT OR IGNORE INTO strike_appeal_data (user_id, strike_appeal_id, department) VALUES (?,?,?)", (ctx.user.id, strike_id, self.department.value))

        embed = Embed(title="New Strike Appeal").add_field(name="Staff member", value="{} | {}".format(ctx.user, ctx.user.id), inline=False).add_field(name="Department", value=self.department.value, inline=True).add_field(name="Reason of Appeal", value=self.strike_appeal.value, inline=False).add_field(name="Strike Appeal ID", value=strike_id, inline=False).set_footer("To accept or deny the appeal, use `/strike verdict STRIKE_APPEAL_ID accept` or `/strike verdict STRIKE_APPEAL_ID deny`")

        channel = self.bot.fetch_channel(1004744695085285457)

        return await channel.send(embed=embed)


class Start_Appeal(ui.View):
    def __init__(self, bot):
        self.bot=bot
        super().__init__(timeout=600)
        self.value = None

    @ui.button(label="Continue", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = True
        await ctx.response.send_modal(Strike_Appeal(self.bot))
        self.stop()
