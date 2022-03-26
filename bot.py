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
intents = discord.Intents.all()
bot = commands.Bot(
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

def fullName(author):
    #Returns name + tag from user/Member object
    logging.debug("call: fullName()")
    return author.name + "#" + author.discriminator

# --Discord Events--
logging.debug("Defining commands...")
@bot.event
async def on_ready():
    """logged in?"""
    logging.debug("call: on_ready()")
    print(f"fishbluebot has logged on in to Discord as {bot.user} with slash commands!")

@bot.listen("on_message")
async def on_message_listener(message):
    #When someone messages
    global msgst
    logging.debug("call: on_message()")

    if message.author == bot.user:
        #Is the author of the message the bot?
        return

    if message.author.bot:
        return

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description="Unknown Command",
            color=discord.Color.red()
        )
        await ctx.followup.send(embed=embed)

    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="You're missing an argument!",
            color=discord.Color.red()
        )
        await ctx.followup.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description="Insufficient permissions!",
            color=discord.Color.red()
        )
        await ctx.followup.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Error",
            description=str(error),
            color=discord.Color.red()
        )
        embed.set_footer(text="Is this a bug? Report it to help make this bot better!")
        await ctx.followup.send(embed=embed)

# --Commands--

@bot.slash_command(guild_ids=[837710846280073279])
async def ping(ctx):
    """Ping"""
    logging.debug("call: ping()")
    await ctx.defer()

    await ctx.followup.send("pong")

@bot.slash_command(guild_ids=[837710846280073279])
async def magic8ball(ctx, *, question):
    """Magic 8-ball. Ask it your questions."""
    logging.debug("call: magic8ball()")
    await ctx.defer()
    global m8answers
    await ctx.followup.send(
        "In response to question \"" + "".join(question) + "\"\n" + m8answers[
            ord(
                os.urandom(
                    1
                )
            ) % len(
                m8answers
            )
        ]
    )

@bot.slash_command(guild_ids=[837710846280073279])
async def killswitch(ctx):
    """Killswitch"""
    logging.debug("call: killswitch()")
    logging.info(f"Someone attempted to kill the bot, ID: {ctx.author.id}")
    await ctx.defer()

    if isAuthorized(ctx.author.id):
        await ctx.followup.send("I am now commiting die.")
        print("ouchie someone killed me")
        logging.warning("Exiting...")
        sys.exit()

    else:
        await ctx.followup.send("rude why are you trying to kill me >:(")

@bot.slash_command(guild_ids=[837710846280073279])
async def kill(ctx, person):
    """Kill people. Idk y."""
    logging.debug("call: kill()")
    await ctx.defer()

    if isMention(person):
        if int(ctx.author.id) == int(idFromMention(person)):
            await ctx.followup.send("Aw c'mon, don't kill yourself.")
            return

    else:
        if person.strip() == ctx.author.name:
            await ctx.followup.send("Aw c'mon, don't kill yourself.")
            return

    if ("@everyone" in person) or ("@here" in person):
        await ctx.followup.send("Mass genocide isn't allowed yet. Try again later.")
        return

    if isMention(person):
        person = await bot.fetch_user(int(idFromMention(person)))
        person = person.name

    else:
        pass

    embed = discord.Embed(
        title=f"{ctx.author.name} has violently murdered {person}!",
        description="oof",
    )
    embed.set_image(url=kawaii("kill"))

    await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[837710846280073279])
async def bruh(ctx):
    """Bruh."""
    logging.debug("call: bruh()")
    await ctx.defer()

    await ctx.followup.send("""██████╗░██████╗░██╗░░░██╗██╗░░██╗░░░
██╔══██╗██╔══██╗██║░░░██║██║░░██║░░░
██████╦╝██████╔╝██║░░░██║███████║░░░
██╔══██╗██╔══██╗██║░░░██║██╔══██║░░░
██████╦╝██║░░██║╚██████╔╝██║░░██║██╗
╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝""")

@bot.slash_command(guild_ids=[837710846280073279])
async def tree(ctx, size=3):
    """Prints little trees."""
    logging.debug("call: tree()")
    await ctx.defer()

    size = int(size)
    if size > 30:
        await ctx.followup.send("DoSing me is illegal at the moment.")
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

        await ctx.followup.send("```" + chr(8203) + out[:-1] + "```")

@bot.slash_command(guild_ids=[837710846280073279])
async def logsclear(ctx):
    """Clears logs of FBB."""
    logging.debug("call: logsclear()")

    if isAuthorized(ctx.author.id):
        with open("latest.log", "w") as f: pass
        await ctx.followup.send("Logs have been erased.")
        print("Logs have been erased.")

    else:
        await ctx.followup.send("You don't have sufficient permissions to run this command.")

@bot.slash_command(guild_ids=[837710846280073279])
async def joke(ctx):
    """Prints a random corny joke."""
    logging.debug("call: joke()")
    await ctx.defer()

    j = await Jokes()
    jk = {}

    while jk == {}:
        jk = await j.get_joke(
            blacklist=[
                "nsfw",
                "racist",
                "sexist"
            ]
        )

    if jk["type"] == "single":
        await ctx.followup.send(jk["joke"])

    else:
        jsetup = await ctx.followup.send(jk["setup"])
        await asyncio.sleep(1)
        await jsetup.edit(jk["setup"] + "\n" + jk["delivery"])

@bot.slash_command(guild_ids=[837710846280073279])
async def coinflip(ctx):
    """Flips a coin."""
    logging.debug("call: coinflip()")
    await ctx.defer()

    if random.randint(0, 1):
        await ctx.followup.send("Heads!")

    else:
        await ctx.followup.send("Tails!")

@bot.slash_command(guild_ids=[837710846280073279])
async def kiss(ctx, person):
    """Kiss people. Idk y."""
    logging.debug("call: kiss()")
    await ctx.defer()

    if isFbb(person):
        await ctx.followup.send("no thank you, I refuse")
        return

    if isMention(person):
        if int(ctx.author.id) == int(idFromMention(person)):
            await ctx.followup.send("wut.")
            return

    else:
        if person.strip() == ctx.author.name:
            await ctx.followup.send("wut.")
            return

    if ("@everyone" in person) or ("@here" in person):
        await ctx.followup.send("oof ur being real amorous here")
        return

    if isMention(person):
        person = await bot.fetch_user(int(idFromMention(person)))
        person = person.name

    else:
        pass

    embed = discord.Embed(
        title=f"{ctx.author.name} has kissed {person}!",
        description="idk what to say tbh",
    )
    embed.set_image(url=kawaii("kiss"))

    await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[837710846280073279])
async def newticket(ctx, *, reason):
    """Allows you to open new tickets."""
    logging.debug("call: newticket()")
    await ctx.defer()

    if len(reason) < 1:
        topic = "unknown topic"

    else:
        topic = "".join(reason)

    ticket_channel = await ctx.guild.create_text_channel(
        f"ticket-{ctx.author.name}-{topic}",
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
    await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[837710846280073279])
async def closeticket(ctx):
    """Allows you to close tickets."""
    logging.debug("call: closeticket()")
    await ctx.defer()

    if ctx.channel.name.startswith("ticket-"):
        await ctx.channel.delete()

    else:
        embed = discord.Embed(
            title="Ticket Creator",
            description="Please run this in the ticket channel you want to close!",
            color = discord.Color.from_rgb(101, 3, 1)
        )
        await ctx.followup.send(embed=embed)

bot.run(
    str(
        os.getenv(
            "DISCORD_TOKEN"
        )
    )
)
