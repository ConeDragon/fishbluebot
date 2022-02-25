# Doesn't support slash commands, probs gonna get yeeted by Discord
#Requirements (to use this script, install v):
#pip install py-cord python-dotenv asyncio pymongo[srv] certifi

#Logging
import logging

with open("latest.log", "w") as f: pass

logging.basicConfig(
    level=logging.DEBUG,
    filename="latest.log",
    format="[%(levelname)s]: %(message)s"
)
logging.debug("1.0.0.2")

#Imports
logging.debug("Importing...")
import discord
import os
import sys
import random
import certifi
import re
import time
import math
import requests
import asyncio

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from pymongo import *
from bson.objectid import ObjectId
from decimal import Decimal
from jokeapi import Jokes

#Import all speedy jsons, use default json module as failsafe
try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json

#Load Environment variables
logging.debug("Loading env...")
load_dotenv()

#Mango- I mean, MongoDB stuff
logging.debug("Opening MongoDB client...")
client = MongoClient(
    str(
        os.getenv(
            "MANGO"
        )
    ),
    tlsCAFile=certifi.where()
)
db = client["FBBDB"]

#Bot stuff
logging.debug("Defining bot constants...")
pf = "fb."
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=pf,
    strip_after_prefix=True,
    intents=intents
)
mentionre = re.compile(r"(.*<@[0-9]+>.*)|(.*<@![0-9]+>.*)")
msgst = {}
kawaiit = "767200055652253719.cTHpJ7bN9V0xFjdK5pWh"

#Reading from file
logging.debug("Reading things from data JSON file...")
with open("dat.json", "r") as f:
    #Load crap from data file
    yeetus = json.loads(f.read())
    m8answers = yeetus["8ball"]
    jokes = yeetus["jokes"]
    del yeetus

# --Functions--
logging.debug("Defining helper functions")
def prec(n):
    return Decimal(str(n))

def bround(n, a=0):
    return prec(
        round(
            prec(
                n
            ),
            a
        )
    )

def isAuthorized(i):
    """Is message author in Authorized? (me or Blue)"""
    logging.debug("call: isAuthorized()")
    if (i == 588132098875850752) or (i == 832740090094682152):
        return True
    
    else:
        return False
    
def isFbb(text):
    """Is text fishbluebot"""
    logging.debug("call: isFbb()")
    text = text.strip()
    if (
        text == str(
            bot.user.name
        )
    ) or (
        text == str(
            bot.user
        )
    ) or (
        text == "<@" + str(
            bot.user.id
        ) + ">"
    ) or (
        text == "<@!" + str(
            bot.user.id
        ) + ">"
    ):
        return True
    
    else:
        return False


def isMention(text):
    #Is text a mention?
    logging.debug("call: isMention()")
    global mentionre
    if mentionre.match(text) == None:
        return False

    else:
        return True


def idFromMention(mention):
    #Get User ID from mention
    logging.debug("call: idFromMention()")
    if mention.startswith("<@!"):
        return str(mention)[3:-1]

    else:
        return str(mention)[2:-1]

def kawaii(sub):
    r = requests.get(f"https://kawaii.red/api/gif/{sub}/token={kawaiit}/")
    return str(r.json()['response'])

# --Discord Events--
logging.debug("Defining commands...")
@bot.event
async def on_ready():
    """logged in?"""
    logging.debug("call: on_ready()")
    print(f"fishbluebot has logged on in to Discord as {bot.user}!")

@bot.event
async def on_message(message):
    #When someone messages
    global msgst
    logging.debug("call: on_message()")

    if message.author == bot.user:
        #Is the author of the message the bot?
        return

    if message.author.bot:
        return #Prevent bots from running commands.

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description="Unknown Command",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="You're missing an argument!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description="Insufficient permissions!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Error",
            description=str(error),
            color=discord.Color.red()
        )
        embed.set_footer(text="Is this a bug? Report it to help make this bot better!")
        await ctx.send(embed=embed)

# --Commands--

@bot.command()
async def ping(ctx):
    """Ping"""
    logging.debug("call: ping()")
    await ctx.send("pong")

@bot.command(aliases=["8ball"])
async def magic8ball(ctx, *args):
    """Magic 8-ball. Ask it your questions."""
    logging.debug("call: magic8ball()")
    global m8answers
    await ctx.send(
        m8answers[
            ord(
                os.urandom(
                    1
                )
            ) % len(
                m8answers
            )
        ]
    )
    
@bot.command()
async def killswitch(ctx):
    """Killswitch"""
    logging.debug("call: killswitch()")
    logging.info(f"Someone attempted to kill the bot, ID: {ctx.message.author.id}")
    if isAuthorized(ctx.message.author.id):
        await ctx.send("I am now commiting die.")
        print("ouchie someone killed me")
        logging.warning("Exiting...")
        sys.exit()
        
    else:
        await ctx.send("rude why are you trying to kill me >:(")

@bot.command()
async def kill(ctx, person):
    """Kill people. Idk y."""
    logging.debug("call: kill()")
    if isMention(person):
        if int(ctx.message.author.id) == int(idFromMention(person)):
            await ctx.send("Aw c'mon, don't kill yourself.")
            return

    else:
        if person.strip() == ctx.message.author.name:
            await ctx.send("Aw c'mon, don't kill yourself.")
            return

    if ("@everyone" in person) or ("@here" in person):
        await ctx.send("Mass genocide isn't allowed yet. Try again later.")
        return

    if isMention(person):
        person = await bot.fetch_user(int(idFromMention(person)))
        person = person.name

    else:
        pass

    embed = discord.Embed(
        title=f"{ctx.message.author.name} has violently murdered {person}!",
        description="oof",
    )
    embed.set_image(url=kawaii("kill"))

    await ctx.send(embed=embed)

@bot.command()
async def bruh(ctx):
    """Bruh."""
    logging.debug("call: bruh()")
    await ctx.send("""██████╗░██████╗░██╗░░░██╗██╗░░██╗░░░
██╔══██╗██╔══██╗██║░░░██║██║░░██║░░░
██████╦╝██████╔╝██║░░░██║███████║░░░
██╔══██╗██╔══██╗██║░░░██║██╔══██║░░░
██████╦╝██║░░██║╚██████╔╝██║░░██║██╗
╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝""")

@bot.command()
async def tree(ctx, size=3):
    """Prints little trees."""
    if size > 30:
        await ctx.send("DoSing me is illegal at the moment.")
        return

    else:
        size = int(size)
        a = 1
        b = 2 * size - 1
        out = ""

        char = "*"

        for i in range(0, size):
            out += "".join([char for j in range(0, a)]).center(b) + "\n"
            a += 2

        for i in range(0, int(math.ceil(size / 20))):
            out += char.center(b) + "\n"

        await ctx.send("```" + chr(8203) + out[:-1] + "```")

@bot.command()
async def logsclear(ctx):
    """Clears logs of FBB."""
    if isAuthorized(ctx.message.author.id):
        with open("latest.log", "w") as f: pass
        await ctx.send("Logs have been erased.")
        print("Logs have been erased.")

    else:
        await ctx.send("You don't have sufficient permissions to run this command.")

@bot.command()
async def joke(ctx):
    """Prints a random corny joke."""
    logging.debug("call: joke()")
    j = await Jokes()
    jk = await j.get_joke(
        blacklist=[
            "nsfw",
            "racist",
            "sexist"
        ]
    )

    if jk["type"] == "single":
        await ctx.send(jk["joke"])

    else:
        await ctx.send(jk["setup"])
        await asyncio.sleep(1)
        await ctx.send(jk["delivery"])

@bot.command()
async def coinflip(ctx):
    """Flips a coin."""
    if random.randint(0, 1):
        await ctx.send("Heads!")

    else:
        await ctx.send("Tails!")

@bot.command()
async def kiss(ctx, person):
    """Kill people. Idk y."""
    logging.debug("call: kill()")
    if isMention(person):
        if int(ctx.message.author.id) == int(idFromMention(person)):
            await ctx.send("wut.")
            return

    else:
        if person.strip() == ctx.message.author.name:
            await ctx.send("wut.")
            return

    if ("@everyone" in person) or ("@here" in person):
        await ctx.send("oof ur being real amorous here")
        return

    if isMention(person):
        person = await bot.fetch_user(int(idFromMention(person)))
        person = person.name

    else:
        pass

    embed = discord.Embed(
        title=f"{ctx.message.author.name} has kissed {person}!",
        description="idk what to say tbh",
    )
    embed.set_image(url=kawaii("kiss"))

    await ctx.send(embed=embed)

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)