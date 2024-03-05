import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# TOKEN = 'MTIxMjg4MzExNjk3NzQzMDYxOQ.GcO2sA.fyM3h-NG2N-SqEiolzAvg_h9gat-yFAuhos5M'o
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is now running.')
    
client.run(TOKEN)