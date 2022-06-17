from os import listdir
from nextcord import Intents
from nextcord.ext.commands import AutoShardedBot as Bot
from config import TOKEN

intents = Intents(guilds=True, members=True, messages=True,
                  typing=True)
bot = Bot(intents=intents)
bot.remove_command('help')

for filename in listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
    print(f"{filename} loaded")
    
  else:
    print(f'Unable to load {filename[:-3]}')


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))


bot.run(TOKEN)
