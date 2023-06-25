import logging
import discord.ext.commands as ds
import discord
from tools import info
import platform
from database import database
import os


logger = logging.getLogger("discord")
bot = ds.Bot(owner_id=info.DeveloperDiscordId, command_prefix="~", intents=discord.Intents.all())
db = None

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info("-------------------")


bot.run(token=info.info["token"], reconnect=True)

