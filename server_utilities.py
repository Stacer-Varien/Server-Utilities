import logging

from discord import Intents, Object
from discord.ext.commands import Bot, when_mentioned_or

from config import BASE_DIR, TOKEN, vhf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def build_intents() -> Intents:
    intents = Intents.none()
    intents.guilds = True
    intents.members = True
    intents.guild_messages = True
    intents.dm_messages = True
    intents.guild_reactions = True
    intents.message_content = True
    return intents


class ServerUtilities(Bot):
    async def setup_hook(self):
        await self.load_extension("jishaku")

        for package in ("shared", "VHF"):
            for path in sorted((BASE_DIR / package).glob("*.py")):
                extension = f"{package}.{path.stem}"
                await self.load_extension(extension)
                logger.info("Loaded extension %s", extension)

        await self.tree.sync()
        await self.tree.sync(guild=Object(id=vhf))
        logger.info("Synced global commands and VHF guild commands")


bot = ServerUtilities(
    intents=build_intents(),
    command_prefix=when_mentioned_or("su!", "SU!", "Su!", "su", "SU", "sU"),
)
bot.remove_command("help")


@bot.event
async def on_ready():
    logger.info("Connected as %s (%s)", bot.user, bot.user.id)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "Missing Discord token. Set DISCORD_TOKEN in the environment or .env file."
        )
    bot.run(TOKEN, log_handler=None)
