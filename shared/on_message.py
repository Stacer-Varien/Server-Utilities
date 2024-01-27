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
        if "discord.gg" in message.content and message.channel.id in no_invites:
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

                punishments = {
                    3: (
                        "2 hour mute",
                        "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied",
                    ),
                    6: (
                        "kick",
                        "Member has reached the 6 warn point punishment. A kick punishment was applied",
                    ),
                    10: (
                        "ban",
                        "Member has reached the 10 warn point punishment. A ban punishment was applied",
                    ),
                }

                if warn_points in punishments:
                    punishment, result_msg = punishments[warn_points]
                    try:
                        punishment_msg = Embed(
                            description=f"You are {punishment} from **{message.guild.name}**\nYou have reached the {warn_points} warn point punishment"
                        )
                        await message.author.send(embed=punishment_msg)
                    except Forbidden:
                        pass

                    if punishment == "2 hour mute":
                        await message.author.edit(
                            timed_out_until=(utcnow() + timedelta(hours=2)),
                            reason="2 hour mute punishment applied",
                        )

                    elif punishment == "kick":
                        await message.author.kick(
                            reason=f"{punishment} punishment applied"
                        )

                    elif punishment == "ban":
                        await message.author.ban(
                            reason=f"{punishment} punishment applied"
                        )

                    result = result_msg
                else:
                    result = "No warn point punishment applied"

                embed.add_field(name="Result", value=result, inline=False)
                embed.set_footer(
                    text="If you feel this warn was a mistake, please use `/appeal WARN_ID`"
                )
                embed.set_thumbnail(url=message.author.display_avatar)
                await adwarn_channel.send(message.author.mention, embed=embed)

        elif message.channel.id == 1041309643449827360:
            attachments = bool(message.attachments)
            content = bool(message.content)
            stickers = bool(message.stickers)

            if (content and not attachments) or (not content and stickers):
                await message.delete()
                return
            if (
                (content and attachments)
                or (attachments and not content)
                or (stickers and attachments)
            ):
                return

        elif (
            message.guild.id == 974028573893595146
            and message.channel.id != 1173932523764600882
            and len(message.attachments) >= 1
        ):
            await message.add_reaction(":mhxaLove:1174261737697050625")


async def setup(bot: Bot):
    await bot.add_cog(AutomodCog(bot))
