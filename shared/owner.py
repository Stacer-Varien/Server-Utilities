from discord.ext.commands import (
    Cog,
    Bot,
    group,
    is_owner,
    guild_only,
    Context,
    Greedy,
    command,
)
from discord import Embed, File, Game, Activity, Object, ActivityType, HTTPException
from os import execv
from sys import executable, argv
from typing import Literal, Optional


def restart_bot():
    execv(executable, ["python"] + argv)


class ownercog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(aliases=["act", "pressence"], invoke_without_command=True)
    @is_owner()
    async def activity(self, ctx: Context):
        embed = Embed(
            title="This is a group command. However, the available commands for this is:",
            description="`activity play ACTIVITY`\n`activity listen ACTIVITY`\n`activity clear`",
        )
        await ctx.send(embed=embed)

    @activity.command(aliases=["playing"])
    @is_owner()
    async def play(self, ctx: Context, *, activity: str):
        await self.bot.change_presence(activity=Game(name=activity))
        await ctx.send(f"I am now playing `{activity}`")

    @activity.command(aliases=["listening"])
    @is_owner()
    async def listen(self, ctx: Context, *, activity: str):
        await self.bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity)
        )
        await ctx.send(f"I am now listening to `{activity}`")

    @activity.command(aliases=["remove", "clean", "stop"])
    @is_owner()
    async def clear(self, ctx: Context):
        await self.bot.change_presence(activity=None)
        await ctx.send(f"I have cleared my activity")

    @command(aliases=["restart", "refresh"])
    @is_owner()
    async def update(self, ctx: Context):
        await ctx.send(f"Now updating")
        restart_bot()

    @command()
    @guild_only()
    @is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
    @command(aliases=["db", "database"])
    @is_owner()
    async def senddb(self, ctx:Context):
        with open('database.db', 'rb') as file:
            try:
                await ctx.author.send(file=File(file))
            except:
                content="""
ERROR!
# Failed to send database! 
        
Make sure private messages between **me and you are opened** or check the server if the database exists"""
                await ctx.send(content)


async def setup(bot: Bot):
    await bot.add_cog(ownercog(bot))
