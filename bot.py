#Imports
import discord
import os

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

@bot.event
async def on_ready():
    #logged in?
    print(f"fishbluebot has logged on in to Discord as {bot.user}!")

bot.run(str(os.getenv("DISCORD_TOKEN")))