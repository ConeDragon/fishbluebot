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
import logging
import time
import math

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from pymongo import *
from bson.objectid import ObjectId
from decimal import Decimal

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

#Reading from file
logging.debug("Reading things from data JSON file...")
with open("dat.json", "r") as f:
    #Load crap from data file
    yeetus = json.loads(f.read())
    m8answers = yeetus["8ball"]
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

def isAuthorized(ctx):
    """Is message author in Authorized? (me or Blue)"""
    logging.debug("call: isAuthorized()")
    if (ctx.message.author.id == 588132098875850752) or (ctx.message.author.id == 832740090094682152):
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
    if isAuthorized(ctx):
        await ctx.send("I am now commiting die.")
        print("ouchie someone killed me")
        logging.warning("Exiting...")
        sys.exit()
        
    else:
        await ctx.send("rude why are you trying to kill me >:(")

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)