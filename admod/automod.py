from nextcord import Embed, Message
from nextcord.ext.commands import Cog, Bot
from config import db
from random import randint
from datetime import timedelta
from nextcord.utils import utcnow
from assets.not_allowed import no_invites, no_nsfw_spam
from assets.functions import give_adwarn_auto, get_warn_points


class automodcog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if 'discord.gg' in message.content:
            if message.channel.id in no_invites:
                if not message.author.bot:
                    await message.delete()
                    warn_id = f"{randint(0,100000)}"
                    appeal_id = f"{randint(0,100000)}"

                    if give_adwarn_auto(message.channel, message.author.id, self.bot.user.id, warn_id, appeal_id) == False:
                        pass
                    else:
                        give_adwarn_auto(
                            message.channel, message.author.id, self.bot.user.id, warn_id, appeal_id)
                        adwarn_channel = message.guild.get_channel(
                            925790260695281703)
                        reason = f"Incorrectly advertising in {message.channel.mention}"

                        warn_points = get_warn_points(message.author.id)

                        embed = Embed(
                            title="You have been warned", color=0xFF0000)
                        embed.add_field(
                            name="Reason of warn", value=reason, inline=True)
                        embed.add_field(
                            name="Warn ID", value=warn_id, inline=True)
                        embed.add_field(name="Warn Points",
                                        value=warn_points, inline=True)

                        if warn_points == 3:
                            await message.author.edit(timeout=utcnow()+timedelta(hours=2), reason="2 hour mute punishment applied")
                            result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"
                            try:
                                timeoutmsg = Embed(
                                    description=f"You have recieved a timeout of 3 hours from **{message.guild.name}**\nYou have reached the 3 warn point punishment")
                                await message.author.send(embed=timeoutmsg)
                            except:
                                pass

                        elif warn_points == 6:
                            try:
                                kickmsg = Embed(
                                    description=f"You are kicked from **{message.guild.name}**\nYou have reached the 6 warn point punishment")
                                await message.author.send(embed=kickmsg)
                            except:
                                pass
                            await message.author.kick(reason="Kick punishment applied")
                            result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                        elif warn_points == 10:
                            try:
                                banmsg = Embed(
                                    description=f"You are banned from **{message.guild.name}**\nYou have reached the 10 warn point punishment")
                                await message.author.send(embed=banmsg)
                            except:
                                pass
                            await message.author.ban(reason="Ban punishment applied")
                            result = "Member has reached the 10 warn point punishment. A ban punishment was applied"

                        else:
                            result = 'No warn point punishment applied'

                        embed.add_field(
                            name="Result", value=result, inline=False)
                        embed.set_footer(
                            text="If you feel this warn was a mistake, please use `/appeal WARN_ID`")
                        embed.set_thumbnail(url=message.author.display_avatar)
                        await adwarn_channel.send(message.author.mention, embed=embed)
                else:
                    pass
        elif message.channel.id == 1041309643449827360:
            attachments = bool(message.attachments)
            content = bool(message.content)

            if content == True and attachments == False:
                await message.delete()
            elif content == True and attachments == True:
                pass
            elif attachments == True and content == False:
                pass
        elif message.channel.id in no_nsfw_spam:
            attachments = bool(message.attachments)
            if attachments == True:
                if len(message.attachments) > 5:
                    await message.channel.send("HEY {}! You are sending too many attachments at once!".format(message.author.mention), delete_after=5)
                    await message.delete()
                else:
                    pass
            else:
                pass


def setup(bot: Bot):
    bot.add_cog(automodcog(bot))
