from datetime import timedelta
from random import randint

from discord import Color, Embed, Message, Forbidden
from discord.ext.commands import Cog, Bot
from discord.utils import utcnow

from assets.buttons import Confirmation
from assets.functions import Warn, LOAMod
from assets.not_allowed import no_invites, no_nsfw_spam, not_allowed_nsfw


class AutomodCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if "discord.gg" in message.content:
            if message.channel.id in no_invites:
                if not message.author.bot:
                    await message.delete()
                    warn_id = randint(0, 100000)
                    warn_data = Warn(message.author, self.bot.user, warn_id)

                    if not warn_data.auto_give(message.channel):
                        return

                    warn_data.auto_give(message.channel)
                    adwarn_channel = message.guild.get_channel(925790260695281703)
                    reason = f"Incorrectly advertising in {message.channel.mention}"

                    warn_points = warn_data.get_points()

                    embed = Embed(title="You have been warned", color=0xFF0000)
                    embed.add_field(name="Reason of warn", value=reason, inline=True)
                    embed.add_field(name="Warn ID", value=warn_id, inline=True)
                    embed.add_field(name="Warn Points", value=warn_points, inline=True)

                    if warn_points == 3:
                        await message.author.edit(
                            timed_out_until=(utcnow() + timedelta(hours=2)),
                            reason="2 hour mute punishment applied",
                        )
                        result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"
                        try:
                            timeoutmsg = Embed(
                                description=f"You have recieved a timeout of 3 hours from **{message.guild.name}**\nYou have reached the 3 warn point punishment"
                            )
                            await message.author.send(embed=timeoutmsg)
                        except Forbidden:
                            pass

                    elif warn_points == 6:
                        try:
                            kickmsg = Embed(
                                description=f"You are kicked from **{message.guild.name}**\nYou have reached the 6 warn point punishment"
                            )
                            await message.author.send(embed=kickmsg)
                        except Forbidden:
                            pass
                        await message.author.kick(reason="Kick punishment applied")
                        result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                    elif warn_points == 10:
                        try:
                            banmsg = Embed(
                                description=f"You are banned from **{message.guild.name}**\nYou have reached the 10 warn point punishment"
                            )
                            await message.author.send(embed=banmsg)
                        except Forbidden:
                            pass
                        await message.author.ban(reason="Ban punishment applied")
                        result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                    else:
                        result = "No warn point punishment applied"

                    embed.add_field(name="Result", value=result, inline=False)
                    embed.set_footer(
                        text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
                    )
                    embed.set_thumbnail(url=message.author.display_avatar)
                    await adwarn_channel.send(message.author.mention, embed=embed)
            return

        if message.channel.id in not_allowed_nsfw:
            await message.delete()
            return

        if message.channel.id == 1041309643449827360:
            attachments = bool(message.attachments)
            content = bool(message.content)

            if content is True and attachments is False:
                await message.delete()
                return
            if (content is True and attachments is True) or (attachments is True and content is False):
                return

        if message.channel.id == 985976000020111440:
            attachments = bool(message.attachments)
            if attachments == True:
                if len(message.attachments) > 5:
                    await message.delete()
                    await message.channel.send(
                        "HEY {}! You are sending too many attachments at once!".format(
                            message.author.mention
                        ),
                        delete_after=5,
                    )


async def setup(bot: Bot):
    await bot.add_cog(AutomodCog(bot))
