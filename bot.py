import discord
import os
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

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

async def fetch_questions(ctx):
    url = "https://opentdb.com/api.php?amount=10&category=23&difficulty=medium&type=multiple"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "results" in data:
            questions = data["results"]
            return questions
    except Exception as e:
        await ctx.send(f"Failed to fetch questions: {e}")
        return None


#@client.event
@bot.event
async def on_ready():
    print(f'{bot.user} is now connected to Discord.')


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

    questions = await fetch_questions(ctx)
    if not questions:
        return

    for question in questions:
        question_text = f'Question: {question["question"]}'
        options = [question["correct_answer"]] + question["incorrect_answers"]
        random.shuffle(options)
        question_text += "\nOptions:\n" + "\n".join([f"{i}. {option}" for i, option in enumerate(options, start=1)])
        await ctx.send(question_text)
        user_choice = None
        while user_choice is None:
            try:
                user_choice = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit(), timeout=30)
                user_choice = int(user_choice.content)
                if user_choice < 1 or user_choice > len(options):
                    await ctx.send(f"Invalid input. Please enter a number between 1 and {len(options)}")
                    user_choice = None
            except asyncio.TimeoutError:
                await ctx.send("Time's up! Quiz aborted.")
                return
            except ValueError:
                await ctx.send("Invalid input. Please enter a number.")
                user_choice = None

        if options[user_choice - 1] == question["correct_answer"]:
            score += 1
            await ctx.send("Correct answer!")
        else:
            await ctx.send(f"Incorrect. The correct answer is: {question['correct_answer']}")
            break

    await ctx.send(f"Quiz over! Your score: {score} out of {len(questions)}.")
    


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
