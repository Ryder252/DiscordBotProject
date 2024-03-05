import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} is now running.')
    
client.run(TOKEN)

# Key features: 
# Menu: 1. Instruction and functions, 