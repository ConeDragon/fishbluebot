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
kawaiit = str(os.getenv("KAWAII"))

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
    print(text)
    text = str(text)
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

@bot.listen("on_message")
async def on_message_listener(message):
    #When someone messages
    global msgst
    logging.debug("call: on_message()")

    if message.author == bot.user:
        #Is the author of the message the bot?
        return

    if message.author.bot:
        return #Prevent bots from running commands.

    if "f%diagnostics%" in message.content:
        # diagnostics
        await message.channel.send("testing... 1 2 3 testing...")

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

@bot.command()
async def pong(ctx):
    """Pong"""
    logging.debug("call: pong()")
    await ctx.send("ping")

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
    logging.debug("call: coinflip()")
    if random.randint(0, 1):
        await ctx.send("Heads!")

    else:
        await ctx.send("Tails!")

@bot.command()
async def kiss(ctx, person):
    """Kiss people. Idk y."""
    logging.debug("call: kiss()")
    if isFbb(person):
        await ctx.send("no thank you, I refuse")
        return

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

@bot.command(aliases=["new-ticket", "new_ticket"])
async def newticket(ctx, *args):
    """Allows you to open new tickets."""
    logging.debug("call: newticket()")
    if len(args) < 1:
        topic = "unknown topic"

    else:
        topic = " ".join(args)

    ticket_channel = await ctx.guild.create_text_channel(
        f"ticket-{ctx.message.author.name}-{topic}",
        category=get(
            bot.get_guild(
                837710846280073279
            ).categories,
            id=956664290553782324
        )
    )
    await ticket_channel.set_permissions(
        ctx.guild.get_role(
            ctx.guild.id
        ),
        send_messages=False,
        read_messages=False
    )

    for role in ctx.guild.roles:
        if role.permissions.manage_guild:
            await ticket_channel.set_permissions(
                role,
                send_messages=True,
                read_messages=True,
                add_reactions=True,
                embed_links=True,
                attach_files=True,
                read_message_history=True,
                external_emojis=True
            )

    await ticket_channel.set_permissions(
        ctx.author,
        send_messages=True,
        read_messages=True,
        add_reactions=True,
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        external_emojis=True
    )
    embed = discord.Embed(
        title="Ticket Creator",
        description=f"Your ticket has been created for {topic}.",
        color=discord.Color.from_rgb(2, 0, 255)
    )
    await ctx.send(embed=embed)

@bot.command(aliases=["close-ticket", "close_ticket"])
async def closeticket(ctx):
    """Allows you to close tickets."""
    logging.debug("call: closeticket()")
    if ctx.channel.name.startswith("ticket-"):
        await ctx.channel.delete()

    else:
        embed = discord.Embed(
            title="Ticket Creator",
            description="Please run this in the ticket channel you want to close!",
            color = discord.Color.from_rgb(101, 3, 1)
        )
        await ctx.send(embed=embed)

@bot.command()
async def slap(ctx, person):
    """Slap people almost to death."""
    logging.debug("call: slap()")
    if isFbb(person):
        await ctx.send("might I recommend this therapist I know to you?")
        return

    if isMention(person):
        if int(ctx.message.author.id) == int(idFromMention(person)):
            await ctx.send("The United States Suicide Prevention Lifeline's phone number is (800) 273-8255")
            return

    else:
        if person.strip() == ctx.message.author.name:
            await ctx.send("The United States Pls Don't Kill Urself Hotline Or Something Idk's phone number is (696) 420-6969")
            return

    if ("@everyone" in person) or ("@here" in person):
        await ctx.send("f u bud (btw mode r gonna kill u for everyone pinging now glhf)")
        return

    if isMention(person):
        person = await bot.fetch_user(int(idFromMention(person)))
        person = person.name

    else:
        pass

    embed = discord.Embed(
        title=f"{ctx.message.author.name} has slapped {person}!",
        description=f"I think {person} needs an ambulance or something",
    )
    embed.set_image(url=kawaii("slap"))

    await ctx.send(embed=embed)

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)
