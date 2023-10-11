import discord
import os
from discord.ext import commands
import requests

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# intents = discord.Intents.default()  # Create an instance of the discord.Intents class
# client = discord.Client(intents=intents)  # Pass the intents object to the discord.Client constructor

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # print(f'Received message: {message.content} from {message.author}')  # Debug print statement
    if message.author == bot.user:
        return

    lower_message = message.content.lower()
    greetings = ['hey pokebot', 'hello pokebot', 'hi pokebot', 'yo pokebot', 'sup pokebot']
    farewells = ['bye pokebot', 'goodbye pokebot', 'see ya pokebot', 'cya pokebot', 'later pokebot']    
    if any(greeting in lower_message for greeting in greetings):
        await message.channel.send('Hey!')
    elif any(farewell in lower_message for farewell in farewells):
        await message.channel.send('Bye!')
    
    await bot.process_commands(message)

@bot.command()
async def guide(ctx):
    await ctx.send("Here are the commands I can respond to:\n"
                   "!pokemon <pokemon name or number> - Get information about a Pokemon\n"
                   "!help - Get a list of commands")

@bot.command()
async def pokemon(ctx, arg):
    try:
        arg_lower = arg.lower()
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{arg_lower}')
        response.raise_for_status()  # Raises a HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        await ctx.send("Sorry, there is no Pokemon by that name.")
        return

    data = response.json()
    name = data['name']
    poke_id = data['id']
    type_name = data['types'][0]['type']['name']
    image_url = data['sprites']['front_default']

    message = f"**Here is the information you requested!**\n" \
              f"# {name.upper()}\n" \
              f"## ID: {poke_id}\n" \
              f"## Type: {type_name}\n" \
              f"{image_url}"
    await ctx.send(message)

bot.run(DISCORD_TOKEN)