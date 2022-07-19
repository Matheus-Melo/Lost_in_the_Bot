import discord
from discord import *
import os
from dotenv import load_dotenv

load_dotenv()

bot_intents = discord.Intents.all()

bot = discord.Bot(intents=bot_intents)


@bot.event
async def on_ready():
    print(f'{bot.user} launched! 🚀')

bot.run(os.getenv('TOKEN'))
