import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

#client = discord.Client(intents=discord.Intents.default())

#@client.event
@bot.event
async def on_ready():
    print(f'{bot.user} is now connected to Discord.')
    '''for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is now connected to {guild.name}(ID: {guild.id})') '''

bot = commands.Bot(command_prefix = '!')

@bot.command(name = 'quote')
#async def quotes(statement):
async def quotes(ctx):
    dialogues = [
        'Imagine a meeting between pre-Nazi Hitler and Bob Ross.',
        'I wonder how the Revolutionary War would play out with the militaries of modern America and Great Britain.',
        'Would hippies have existed as we know them today if America never went to Vietnam?'
    ]    
    response = random.choice(dialogues)
    await ctx.send(response)
   #await statement.send(response)    

@bot.command(name='startquiz')
async def start_quiz(ctx):
    # Replace this with your quiz start logic
    await ctx.send("Quiz started! Good luck!")


@bot.command(name='instructions')
async def show_instructions(ctx):
    instructions = (
        "Welcome to the History Quiz Bot!\n\n"
        "To start the quiz, use the command `!startquiz`.\n"
        "You'll be presented with a series of questions related to history.\n"
        "Answer each question to the best of your knowledge!\n\n"
        "Enjoy the quiz and have fun!"
    )
    await ctx.send(instructions)

@bot.command(name='exit')
async def exit_bot(ctx):
    await ctx.send("Goodbye! Thanks for playing the History Quiz Bot.")
    await bot.close()    


bot.run(TOKEN)

# Key features: 
# Menu: 1. Instruction and functions, 

"""
def run_client():
     #TOKEN = 'MTIxMjg4MzExNjk3NzQzMDYxOQ.GcO2sA.fyM3h-NG2N-SqEiolzAvg_h9gat-yFAuhos5M'o
     client = discord.Client()

     @client.event
     async def on_ready():
         print(f'{client.user} is now running.')

     async def on_message(message):
          if message.author == client.user:
               return
           
          if message.content.startswith('$hello'):
               await message.channel.send('Hello!!') 

     client.run(TOKEN) """