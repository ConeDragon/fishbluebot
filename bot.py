#Imports
#Requirements:
#pip install py-cord dotenv pymongo
import discord
import os
import sys
import random
import certifi

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from pymongo import *

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

#Bot stuff
pf = "fb."
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=pf,
    strip_after_prefix=True,
    intents=intents
)

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
    if (text == str(bot.user.name)) or (text == str(bot.user)) or (text == "<@" + str(bot.user.id) + ">") or (text == "<@!" + str(bot.user.id) + ">"):
        return True
    
    else:
        return False

# --Commands--

@bot.event
async def on_ready():
    """logged in?"""
    print(f"fishbluebot has logged on in to Discord as {bot.user}!")

@bot.command()
async def ping(ctx):
    """Ping"""
    await ctx.send("pong")

@bot.command(aliases=["8ball"])
async def magic8ball(ctx, *args):
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

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)