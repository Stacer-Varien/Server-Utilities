from discord import Color, Embed, Message
from discord.ext.commands import Cog, Bot
from assets.functions import Warn, LOAMod
from assets.buttons import Confirmation
from random import randint
from datetime import timedelta
from discord.utils import utcnow
from assets.not_allowed import no_invites, no_nsfw_spam, not_allowed_nsfw


class automodcog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if "discord.gg" in message.content:
            if message.channel.id in no_invites:
                if not message.author.bot:
                    await message.delete()
                    warn_id = f"{randint(0,100000)}"
                    warn_data = Warn(message.author, self.bot.user, warn_id)

                    if warn_data.auto_give(message.channel) == False:
                        pass
                    else:
                        warn_data.auto_give(message.channel)
                        adwarn_channel = message.guild.get_channel(925790260695281703)
                        reason = f"Incorrectly advertising in {message.channel.mention}"

                        warn_points = warn_data.get_points()

                        embed = Embed(title="You have been warned", color=0xFF0000)
                        embed.add_field(
                            name="Reason of warn", value=reason, inline=True
                        )
                        embed.add_field(name="Warn ID", value=warn_id, inline=True)
                        embed.add_field(
                            name="Warn Points", value=warn_points, inline=True
                        )

                        if warn_points == 3:
                            await message.author.edit(
                                timeout=utcnow() + timedelta(hours=2),
                                reason="2 hour mute punishment applied",
                            )
                            result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"
                            try:
                                timeoutmsg = Embed(
                                    description=f"You have recieved a timeout of 3 hours from **{message.guild.name}**\nYou have reached the 3 warn point punishment"
                                )
                                await message.author.send(embed=timeoutmsg)
                            except:
                                pass

                        elif warn_points == 6:
                            try:
                                kickmsg = Embed(
                                    description=f"You are kicked from **{message.guild.name}**\nYou have reached the 6 warn point punishment"
                                )
                                await message.author.send(embed=kickmsg)
                            except:
                                pass
                            await message.author.kick(reason="Kick punishment applied")
                            result = "Member has reached the 6 warn point punishment. A kick punishment was applied"

                        elif warn_points == 10:
                            try:
                                banmsg = Embed(
                                    description=f"You are banned from **{message.guild.name}**\nYou have reached the 10 warn point punishment"
                                )
                                await message.author.send(embed=banmsg)
                            except:
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
                else:
                    pass
            elif message.channel.id in not_allowed_nsfw:
                await message.delete()
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
                    await message.delete()
                    await message.channel.send(
                        "HEY {}! You are sending too many attachments at once!".format(
                            message.author.mention
                        ),
                        delete_after=5,
                    )
        elif message.channel.id == 954594959074418738:
            if not message.author.bot:
                data = LOAMod(message.author)
                view = Confirmation(message.author)
                m_url = message.jump_url

                if message.content.lower().startswith("w!t"):
                    action = "Timeout"
                elif message.content.lower().startswith("w!san"):
                    action = "Sanitize"
                elif message.content.lower().startswith("w!k"):
                    action = "Kick"
                elif message.content.lower().startswith("w!b"):
                    action = "Ban"
                elif message.content.lower().startswith(
                    "w!hb"
                ) or message.content.lower().startswith("w!hackban"):
                    action = "Hackban"
                elif message.content.lower().startswith("w!wa"):
                    action = "Warn"
                else:
                    return

                embed = Embed(
                    description=f"You have used a {action} command.\nDid the command successfully execute?"
                )
                m = await message.channel.send(embed=embed, view=view)

                await view.wait()

                if view.value == True:
                    data.add_wick_action_point()
                    embed = Embed(title=f"Wick {action} command used", color=Color.blue())
                    embed.add_field(
                        name="Used by",
                        value=f"{message.author.mention} | {message.author} | {message.author.id}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Executed command",
                        value=f"{message.content}\n[Click here if the message still exists]({m_url})",
                        inline=False,
                    )
                    embed.set_thumbnail(url=message.author.avatar)
                    log_ch = await self.bot.fetch_channel(1097695442252349500)
                    added = Embed(
                        description="Confirmation complete. This message will be deleted.",
                        color=Color.green(),
                    )
                    await m.edit(embed=added, view=None, delete_after=5)
                    await log_ch.send(embed=embed)

                elif view.value == False:
                    added = Embed(
                        description="Confirmation completed. This message will be deleted.",
                        color=Color.green(),
                    )
                    await m.edit(embed=added, view=None, delete_after=5)

                else:
                    added = Embed(
                        description="No confirmation. This message will be deleted.",
                        color=Color.red(),
                    )
                    await m.edit(embed=added, view=None, delete_after=5)
                await self.bot.process_commands(message)


async def setup(bot: Bot):
    await bot.add_cog(automodcog(bot))
