import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is now connected to {guild.name}(ID: {guild.id})')

bot = commands.Bot(command_prefix = '!')

@bot.command(name = 'quote')
async def quotes(statement):
    dialogues = [
        'Imagine a meeting between pre-Nazi Hitler and Bob Ross.',
        'I wonder how the Revolutionary War would play out with the militaries of modern America and Great Britain.',
        'Would hippies have existed as we know them today if America never went to Vietnam?'
    ]    
    response = random.choice(dialogues)
    await statement.send(response)    

client.run(TOKEN)

# Key features: 
# Menu: 1. Instruction and functions, 