#Imports
#Requirements (to use this script, install v):
#pip install py-cord python-dotenv asyncio pymongo[srv] certifi
import discord
import os
import sys
import random
import certifi
import re

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from pymongo import *
from bson.objectid import ObjectId

#Import all speedy jsons, use default json module as failsafe
try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json

#Load Environment variables
load_dotenv()

#Mango- I mean, MongoDB stuff
client = MongoClient(
    str(
        os.getenv(
            "MANGO"
        )
    ),
    tlsCAFile=certifi.where()
)
db = client["FBBDB"]
pointsc = db["points"]
pointsid = "620cfe72f63ae0339129c774"

#Bot stuff
pf = "fb."
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=pf,
    strip_after_prefix=True,
    intents=intents
)
mentionre = re.compile(r"(.*<@[0-9]+>.*)|(.*<@![0-9]+>.*)")

#Reading from file
with open("dat.json", "r") as f:
    #Load crap from data file
    yeetus = json.loads(f.read())
    m8answers = yeetus["8ball"]
    del yeetus

# --Functions--

def isAuthorized(ctx):
    """Is message author in Authorized? (me or Blue)"""
    if (ctx.message.author.id == 588132098875850752) or (ctx.message.author.id == 832740090094682152):
        return True
    
    else:
        return False
    
def isFbb(text):
    """Is text fishbluebot"""
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
    global mentionre
    if mentionre.match(text) == None:
        return False

    else:
        return True


def idFromMention(mention):
    #Get User ID from mention
    if mention.startswith("<@!"):
        return str(mention)[3:-1]

    else:
        return str(mention)[2:-1]

# --Commands--

@bot.event
async def on_ready():
    """logged in?"""
    print(f"fishbluebot has logged on in to Discord as {bot.user}!")

@bot.event
async def on_message(message):
    #When someone messages
    if message.author == bot.user:
        #Is the author of the message the bot?
        return
    
    tempd = pointsc.find_one(
        {
            "_id": ObjectId(pointsid)
        }
    )
    
    try:
        tempd[str(message.author.id)] += 10
        
    except KeyError:
        tempd[str(message.author.id)] = 10
    
    pointsc.delete_one(
        {
            "_id": ObjectId(pointsid)
        }
    )
    
    pointsc.insert_one(tempd)
    
    await bot.process_commands(message)
    
@bot.command()
async def ping(ctx):
    """Ping"""
    await ctx.send("pong")

@bot.command(aliases=["8ball"])
async def magic8ball(ctx, *args):
    """Magic 8 ball. Ask it your questions."""
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
    if isAuthorized(ctx):
        await ctx.send("I am now commiting die.")
        print("ouchie someone killed me")
        sys.exit()
        
    else:
        await ctx.send("rude why are you trying to kill me >:(")

@bot.command()
async def points(ctx, user=None):
    """Show number of points of others, or yourself."""
    if user == None:
        user = ctx.message.author.id

    elif not isMention(user):
        await ctx.send("That person isn't a mention.")
        return

    else:
        user = idFromMention(user)

    tempd = pointsc.find_one(
        {
            "_id": ObjectId(pointsid)
        }
    )

    try:
        await ctx.send(f"{tempd[str(user)]} points.")

    except KeyError:
        await ctx.send("0 points.")

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)