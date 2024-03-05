import discord
import os
import random
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    dialogues = [
        'Imagine a meeting between pre-Nazi Hitler and Bob Ross.',
        'I wonder how the Revolutionary War would play out with the militaries of modern America and Great Britain.',
        'Would hippies have existed as we know them today if America never went to Vietnam?'
    ]    
    if message.content == '!quote':
        response = random.choice(dialogues)
        await message.channel.send(response)    

client.run(TOKEN)

# Key features: 
# Menu: 1. Instruction and functions, 