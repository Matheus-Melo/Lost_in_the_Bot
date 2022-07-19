import discord
from discord import *
import os
from dotenv import load_dotenv
from configManager import configManager

load_dotenv()

bot_intents = discord.Intents.all()

bot = discord.Bot(intents=bot_intents)


@bot.event
async def on_ready():
    print(f'{bot.user} launched! 🚀')


@bot.event
async def on_message(message):

    #* ignore messages sent from the bot itself, ignore channels that aren't the default
    if message.author == bot.user or message.channel.id != int(configManager().config['DEFAULT']['chat_id']):
        return

    if message.content == ('!bot'):
        await message.channel.send(bot.user)

bot.run(os.getenv('TOKEN'))
