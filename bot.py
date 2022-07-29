import discord
from discord import *
import os
from dotenv import load_dotenv
from myView import myView
from configManager import configManager
from player import Player

load_dotenv()

bot_intents = discord.Intents.all()

bot = discord.Bot(intents=bot_intents)


@bot.event
async def on_ready():
    print(f'{bot.user} launched! 🚀')


@bot.event
async def on_message(message: discord.Message):

    #* ignore messages sent from the bot itself, ignore channels that aren't the default
    if message.author == bot.user or message.channel.id != int(configManager().config['DEFAULT']['chat_id']):
        return

    if message.content == ('!bot'):
        # await message.channel.send(bot.user) #? task 4, respond message with discord name
        author = message.author

        player = Player(
            discord_id = author.id,
            name = author.name,
            level = 1,
            health = 250,
            max_health = 250,
            experience = 0,
            silver = 0
        )
        
        #* display myView when user types '!bot'
        await message.channel.send(view = myView(user=message.author))


bot.run(os.getenv('TOKEN'))
