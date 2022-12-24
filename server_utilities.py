from os import listdir

from nextcord import Intents
from nextcord.ext.commands import Bot

from config import TOKEN

intents = Intents().all()
intents.presences = False
intents.voice_states = False
intents.reactions = False
intents.scheduled_events = False

bot = Bot(intents=intents)
bot.remove_command('help')

for filename in listdir('./HA'):
    if filename.endswith('.py'):
        bot.load_extension(f'HA.{filename[:-3]}')
        print(f"{filename} loaded")
    else:
        print(f'Unable to load {filename[:-3]}')

for filename in listdir('./admod'):
    if filename.endswith('.py'):
        bot.load_extension(f'admod.{filename[:-3]}')
        print(f"{filename} loaded")
    else:
        print(f'Unable to load {filename[:-3]}')

for filename in listdir('./LOA'):
    if filename.endswith('.py'):
        bot.load_extension(f'LOA.{filename[:-3]}')
        print(f"{filename} loaded")

    else:
        print(f'Unable to load {filename[:-3]}')

for filename in listdir('./shared'):
    if filename.endswith('.py'):
        bot.load_extension(f'shared.{filename[:-3]}')
        print(f"{filename} loaded")

    else:
        print(f'Unable to load {filename[:-3]}')

for filename in listdir('./VHF'):
    if filename.endswith('.py'):
        bot.load_extension(f'VHF.{filename[:-3]}')
        print(f"{filename} loaded")

    else:
        print(f'Unable to load {filename[:-3]}')


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN)
