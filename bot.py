import discord
import os
from dotenv import load_dotenv
import random
import requests
import asyncio
import datetime
from discord.ext import commands


# Load environment variables from .env file
load_dotenv()

# Get Discord token and guild from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Define intents
intents = discord.Intents.default()
# Initialize the bot with intents
bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
start_time = datetime.datetime.utcnow()

# Display message upon successful connection to Discord
@bot.event
async def on_ready():
    print(f'Huzzah! {bot.user} is now connected to Discord.')

# Display bot uptime
@bot.command(name = 'uptime')
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - start_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"History Quiz Bot has been up for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")

# Display list of current users    
@bot.command(name = 'userlist')
async def user_list(ctx):
    guild = ctx.guild
    member_list = guild.members
    usernames = [member.name for member in member_list]
    await ctx.send(f'Current listing of users:\n-----------------------------\n{"\n".join(usernames)}')
    
# Command to generate random historical quotes
@bot.command(name = 'quote')
async def quotes(ctx):
    dialogues = [
        '\"A house divided against itself cannot stand.\"\n\t~ Abraham Lincoln',
        '\"I am opposed to any form of tyranny over the mind of man.\"\n\t~ Thomas Jefferson',
        '\"We hold these truths to be self-evident: that all men and women are created equal.\"\n\t~ Elizabeth Cady Stanton',
        '\"My fellow Americans, ask not what your country can do for you, ask what you can do for your country.\"\n\t~ John F. Kennedy',
        '\"I have a dream that one day this nation will rise up and live out the true meaning of its creed; We hold these truths to be self-evident: that all men are created equal.\"\n\t~ Martin Luther King, Jr.'
    ]    
    response = random.choice(dialogues)
    await ctx.send(response)   

# Initialize score variable
score = 0  

# Command to display quiz instructions
@bot.command(name='instructions')
async def show_instructions(ctx):
    instructions = (
        "Welcome to the World History Quiz and Quote Bot!\n\n"
        "To call on a quote, use the command `!quote`.\n"
        "To start the quiz, use the command `!startquiz`.\n"
        "To exit from the bot, use the command `!exit`.\n"
        "You'll be presented with a series of questions related to history.\n"
        "You must answer all the question correctly in order to pass the quiz!.\n"
        "You have 60 seconds to answer a question before the timer runs out.\n"
        "Each time you get a question wrong, the quiz ends.\n"
        "Enjoy the quiz and have fun!"
    )
    await ctx.send(instructions)

async def fetch_questions(ctx):
    url = "https://opentdb.com/api.php?amount=10&category=23&difficulty=easy&type=multiple"
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

# Command to start the quiz
@bot.command(name='startquiz')
async def start_quiz(ctx):
    global score  # Access the global score variable
    score = 0  # Reset score when starting a new quiz

    await ctx.send("Welcome to the History Quiz Bot! Get ready to answer some history questions.")

    questions = await fetch_questions(ctx)
    if not questions:
        return
    
    # Iterate through questions
    for question in questions:
        question_text = f'Question: {question["question"]}'
        options = [question["correct_answer"]] + question["incorrect_answers"]
        random.shuffle(options)
        question_text += "\nOptions:\n" + "\n".join([f"{i}. {option}" for i, option in enumerate(options, start=1)])
        await ctx.send(question_text)

        user_choice = None
        while user_choice is None:
            try:
                # Wait for user input
                user_choice = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit(), timeout=60)
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
               
        # Check for correct answer
        if options[user_choice - 1] == question["correct_answer"]:
            score += 1 # Increment score only if answer is correct
            await ctx.send("Correct answer!")
        else:
            await ctx.send(f"Incorrect. The correct answer is: {question['correct_answer']}")
            break  # Exit loop if answer is incorrect

    # Display final score
    await ctx.send(f"Quiz over! Your score: {score} out of {len(questions)}.")
        
    # Shuffle the questions to randomize their order
    ## random.shuffle(questions)
 
# Command to exit the bot
@bot.command(name='exit')
async def exit_bot(ctx):
    await ctx.send("Goodbye! Thanks for playing the History Quiz Bot.")
    await bot.close()

bot.run(TOKEN)