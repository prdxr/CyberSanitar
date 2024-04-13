# This example requires the 'message_content' intent.

import os
import discord
from discord.ext import commands
from settings import *

bot = commands.Bot(command_prefix='s!', intents=discord.Intents.default())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
