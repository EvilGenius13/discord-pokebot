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
        error_embed = discord.Embed(
            title="Not Found",
            description="Sorry, there is no Pokemon by that name.",
            color=discord.Color.red()
        )
        error_embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png")
        await ctx.send(embed=error_embed)
        return

    data = response.json()
    name = data['name']
    poke_id = data['id']
    type_name = data['types'][0]['type']['name'].upper()  # Convert type to uppercase
    image_url = data['sprites']['front_default']

    # Extracting abilities and converting to uppercase
    abilities = [ability['ability']['name'].upper() for ability in data['abilities']]
    ability_list = ", ".join(abilities[:2]) if len(abilities) > 2 else ", ".join(abilities)

    # Extracting stats
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    hp = stats.get('hp', '-')
    attack = stats.get('attack', '-')
    defense = stats.get('defense', '-')
    speed = stats.get('speed', '-')
    stat_string = f"HP: {hp} | ATK: {attack} | DEF: {defense} | SPD: {speed}"

    # Creating the embed
    embed = discord.Embed(
        title=f"{name.upper()}",
        description=f"#{poke_id}", 
        color=discord.Color.blue()
    )
    embed.set_image(url=image_url)
    embed.add_field(name="Type", value=type_name, inline=True)
    embed.add_field(name="Abilities", value=ability_list, inline=True)
    embed.add_field(name="Stats", value=stat_string, inline=False)

    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)