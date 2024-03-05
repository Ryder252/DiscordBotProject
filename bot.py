import discord

def run_client():
     TOKEN = 'MTIxMjg4MzExNjk3NzQzMDYxOQ.GcO2sA.fyM3h-NG2N-SqEiolzAvg_h9gat-yFAuhos5Mo'
     client = discord.Client()

     @client.event
     async def on_ready():
         print(f'{client.user} is now running.')

     async def on_message(message):
          if message.author == client.user:
               return
           
          if message.content.startswith('$hello'):
               await message.channel.send('Hello!!') 

     client.run(TOKEN)