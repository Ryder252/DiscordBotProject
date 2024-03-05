import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get Discord token and guild from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Define intents
intents = discord.Intents.default()
# Initialize the bot with intents
bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

# Initialize score variable
score = 0  

#bot = commands.Bot(command_prefix='!')
#client = discord.Client(intents=discord.Intents.default())

#@client.event
@bot.event
async def on_ready():
    print(f'{bot.user} is now connected to Discord.')
    '''for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is now connected to {guild.name}(ID: {guild.id})') '''

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

# Command to generate random quotes
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

# Command to start the quiz
@bot.command(name='startquiz')
async def start_quiz(ctx):
    global score  # Access the global score variable
    score = 0  # Reset score when starting a new quiz
    await ctx.send("Welcome to the History Quiz Bot! Get ready to answer some history questions.")
    await ctx.send("Type '!answer' followed by your answer to each question.")

    questions = [
        {
            "question": "Who was the first president of the United States?",
            "correct_answer": "George Washington"
        },
        {
            "question": "In which year did World War II end?",
            "correct_answer": "1945"
        }
        # Add more questions here...
    ] 

    # Shuffle the questions to randomize their order
    random.shuffle(questions)

    for question_data in questions:
        question_text = f'Question: {question_data["question"]}'
        await ctx.send(question_text)
        answer = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if answer.content.lower() == question_data["correct_answer"].lower():
            score += 1  # Increment score if the answer is correct
        else:
             # Notify user of incorrect answer and show the correct answer
            await ctx.send(f"Sorry, that's inncorrect. The correct answer is: {question_data['correct_answer']}")
            break  # End the quiz if the answer is incorrect

        await ctx.send(f"Quiz over! Your score: {score} out of {len(questions)}.")

# Command to display quiz instructions
@bot.command(name='instructions')
async def show_instructions(ctx):
    instructions = (
        "Welcome to the History Quiz Bot!\n\n"
        "To start the quiz, use the command `!startquiz`.\n"
        "You'll be presented with a series of questions related to history.\n"
        "You must answer all the question correctly in order to pass the quiz!.\n"
        "Each time you get a question wrong, the quiz ends.\n"
        "The more questions answered the harder the quiz gets!\n\n"
        "Enjoy the quiz and have fun!"
    )
    await ctx.send(instructions)

# Command to exit the bot
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