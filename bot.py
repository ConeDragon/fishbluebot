#Imports
import discord
import os
import sys

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

#Load Environment variables
load_dotenv()

#Bot stuff
pf = "fb."
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=pf,
    strip_after_prefix=True,
    intents=intents
)

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
    
@bot.command()
async def killswitch(ctx):
    """Killswitch"""
    if isAuthorized(ctx):
        await ctx.send("I am now commiting die.")
        print("ouchie someone killed me")
        sys.exit()
        
    else:
        await ctx.send("rude why are you trying to kill me >:(")

bot.run(str(os.getenv("DISCORD_TOKEN")))