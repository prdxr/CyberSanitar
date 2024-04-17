# This example requires the 'message_content' intent.
import asyncio
import os
import discord
from discord.ext import commands
from settings import *


async def prepare():
    bot = commands.Bot(command_prefix='s!', intents=discord.Intents.all())

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loading {filename}')

    return bot


if __name__ == '__main__':
    bot = asyncio.run(prepare())
    bot.run(BOT_TOKEN)
