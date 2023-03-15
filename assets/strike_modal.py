from discord import *
from discord.ext.commands import Bot
from assets.functions import Strike
from config import db


class Strike_Appeal(ui.Modal, title="Strike Appeal Form"):

    def __init__(self, bot: Bot, strike_id, department):
        super().__init__()
        self.bot = bot
        self.strike_id = strike_id
        self.department = department

    strike_appeal = ui.TextInput(label="Reason for appealling strike",
                                          min_length=4,
                                          max_length=1024,
                                          required=True,
                                          placeholder="Enter your reason here",
                                          style=TextStyle.paragraph)


    async def on_submit(self, ctx: Interaction) -> None:
        embed = Embed(title="New Strike Appeal")
        embed.add_field(name="Staff member",
                        value="{} | {}".format(ctx.user, ctx.user.id),
                        inline=False)
        embed.add_field(name="Department", value=self.department, inline=True)
        embed.add_field(name="Reason of Appeal",
                        value=self.strike_appeal.value,
                        inline=False)
        embed.add_field(name="Strike ID", value=self.strike_id, inline=False)
        embed.set_footer(
            text=
            "To accept or deny the appeal, use `/verdict STRIKE_ID accept` or `/strike verdict STRIKE_ID deny`"
        )
        db.commit()
        channel = self.bot.get_channel(1004744695085285457)

        await channel.send(embed=embed)
        await ctx.response.send_message('Your strike appeal has been logged. Please wait for the appropriate staff to decide if its approvable or not.\nThank you', ephemeral=True)
