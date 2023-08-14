import logging
import discord.ext.commands as ds
import discord
from tools.info import TOKEN, DeveloperDiscordId
import platform
import ffmpeg.player as player
import os
from database.Interfaces import queue


logger = logging.getLogger("discord")
bot = ds.Bot(owner_id=DeveloperDiscordId, command_prefix="~", intents=discord.Intents.all())
db = None
voiceClient: discord.VoiceClient
songQueue = queue.Interface()


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info("-------------------")


@bot.command()
async def join(message:  discord.Message):
    global voiceClient
    voiceClient = await message.author.voice.channel.connect()


@bot.command()
async def play(message: discord.Message, *args: str):
    global voiceClient
    global songQueue
    global logger
    async with message.channel.typing():
        repeat = 0
        if args[-1].startswith("repeat="):
            args, repeat = args[:-1], int(args[-1][7:])
        elif args[-1].startswith("r="):
            args, repeat = args[:-1], int(args[-1][2:])
        songName = " ".join(args)
        logger.info(f'Received to play "{songName}", {repeat+1} times')

        if not bot.voice_clients:
            await join(message)

    await player.play(url=songName,  client=bot, voice_client=voiceClient, Queue=songQueue, msg=message)


@bot.command()
async def stop(message):
    global voiceClient
    voiceClient.stop()
    logger.info("Stopped playing tracks...")
    await voiceClient.disconnect()


@bot.command()
async def skip(message):
    global voiceClient
    voiceClient.stop()
    logger.info("Skipped track...")


@bot.command()
async def queue(message: discord.Message):
    global songQueue
    if songQueue:
        await message.channel.send(content=songQueue.get())
    else:
        await message.channel.send("Очередь пуста")



bot.run(token=TOKEN, reconnect=True)

