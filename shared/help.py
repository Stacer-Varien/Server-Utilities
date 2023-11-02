from typing import List
from discord import (
    Color,
    Embed,
    Interaction,
    app_commands as Serverutil,
)
from discord.ext.commands import GroupCog, Bot


class HelpGroup(GroupCog, name="help"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def command_choices(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Serverutil.Choice[str]]:
        cmds = [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Serverutil.Group)
        ]
        return [
            Serverutil.Choice(name=command, value=command)
            for command in cmds
            if current.lower() in command.lower()
        ]

    @Serverutil.command(description="Get help of a certain command")
    @Serverutil.autocomplete(command=command_choices)
    @Serverutil.describe(command="Which command you need help with?")
    async def command(self, ctx: Interaction, command: Serverutil.Range[str, 3]):
        await ctx.response.defer()
        cmd = [
            cmd
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Serverutil.Group)
            if cmd.qualified_name == command
        ][0]

        bot_perms: dict = (
            cmd.checks[0].__closure__[0].cell_contents
            if len(cmd.checks) > 0
            and cmd.checks[0].__qualname__ == "bot_has_permissions.<locals>.predicate"
            else (
                cmd.checks[1].__closure__[0].cell_contents
                if len(cmd.checks) >= 2
                and cmd.checks[1].__qualname__
                == "bot_has_permissions.<locals>.predicate"
                else None
            )
        )

        member_perms = (
            cmd.checks[0].__closure__[0].cell_contents
            if len(cmd.checks) >= 1
            and cmd.checks[0].__qualname__ == "has_permissions.<locals>.predicate"
            else (
                cmd.checks[1].__closure__[0].cell_contents
                if len(cmd.checks) >= 2
                and cmd.checks[1].__qualname__ == "has_permissions.<locals>.predicate"
                else None
            )
        )

        embed = Embed(title=f"{command.title()} Help", color=Color.random())
        embed.description = cmd.description
        parms = []
        descs = []
        if len(cmd.parameters) > 0:
            for i in cmd.parameters:
                parm = f"[{i.name}]" if i.required is True else f"<{i.name}>"
                desc = f"`{parm}` - {i.description}"
                parms.append(parm)
                descs.append(desc)
            embed.add_field(name="Parameters", value="\n".join(descs), inline=False)

        if bot_perms:
            perms = []
            for i in list(bot_perms.keys()):
                perms.append(str(i).replace("_", " ").title())
            embed.add_field(name="Bot Permissions", value="\n".join(perms), inline=True)

        if member_perms:
            perms = []
            for i in list(member_perms.keys()):
                perms.append(str(i).replace("_", " ").title())
            embed.add_field(
                name="User Permissions", value="\n".join(perms), inline=True
            )

        cmd_usage = "/" + cmd.qualified_name + " " + " ".join(parms)
        embed.add_field(name="Command Usage", value=f"`{cmd_usage}`", inline=False)
        embed.set_footer(
            text="Legend:\n[] - Required\n<> - Optional"
        )

        await ctx.followup.send(embed=embed)

    @command.error
    async def command_error(self, ctx: Interaction, error: Serverutil.AppCommandError):
        if isinstance(error, Serverutil.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            embed = Embed(description="I don't have this command", color=Color.red())
            await ctx.followup.send(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(HelpGroup(bot))
