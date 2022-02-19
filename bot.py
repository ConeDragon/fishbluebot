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
pointsc = db["points"]
pointsid = "620cfe72f63ae0339129c774"

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


# --Commands--
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
        return

    try:
        dif = round(time.time() - msgst[message.author.id])
        msgst[message.author.id] = time.time()

    except KeyError:
        msgst[message.author.id] = time.time()
        dif = 9 #Could be any number >1

    if dif > 1:
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

@bot.command()
async def points(ctx, user=None, silent=False):
    """Show number of points of others, or yourself."""
    logging.debug("call: points()")
    if user == None:
        user = ctx.message.author.id

    elif not isMention(user):
        if not silent:
            await ctx.send("That person isn't a mention.")

        else:
            logging.info("That person isn't a mention (callback from points())")
        return

    else:
        user = idFromMention(user)

    tempd = pointsc.find_one(
        {
            "_id": ObjectId(pointsid)
        }
    )

    try:
        out = f"{tempd[str(user)]} points"

    except KeyError:
        out = "0 points"

    if not silent:
        await ctx.send(out)

    else:
        return out

@bot.command(aliases=["lb"])
async def leaderboard(ctx):
    """Leaderboard function for points."""
    logging.debug("call: leaderboard()")
    global output, thingy
    tempd = pointsc.find_one(
        {
            "_id": ObjectId(pointsid)
        }
    )
    del tempd["_id"]
    thingy = [[k, v] for k, v in tempd.items()]
    thingy = sorted(thingy, key=lambda x: x[1])[::-1]

    output = ""
    async def add(a, n):
        global output, thingy
        try:
            temp = await bot.fetch_user(thingy[n][0])

            if temp.bot:
                del thingy[n]
                await add(a, n)
                return

            output += f"{str(a) + str(temp.name)} - {str(thingy[n][1])} points\n"
            del temp
            return 0

        except (KeyError) as error:
            logging.debug("Error occured in leaderboard.add(), could be incomplete leaderboard")
            logging.warning(f"{type(error).name}: {str(error)}")
            return 1

        except Exception as error:
            logging.debug("Unexpected error occured in leaderboard.add().")
            logging.error(f"{type(error).name}: {str(error)}")
            return 1

    if not await add("🥇", 0):
        if not await add("🥈", 1):
            if not await add("🥉", 2):
                if not await add("🏵️", 3):
                    await add("🏵️", 4)

    curp = await points(ctx, silent=True)
    output += f"{ctx.message.author.name} - {curp}"

    await ctx.send(output)

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)