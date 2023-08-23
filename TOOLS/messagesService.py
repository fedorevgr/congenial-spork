import asyncio

import discord
import logging
import platform
import os
import TOOLS.tools as computations
from TOOLS.info import ffmpegEXEpath
from random import choice

logger = logging.getLogger("discord")


def logOnStartUp(bot):
    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"Logged on servers:\n{' '.join(str(e.name)+': '+str(e.id) for e in bot.guilds)}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info(f"Working directory: " + '/'.join(os.getcwd().split('\\')))
    logger.info("-------------------")


def onNowPlaying(elem, Queue):
    logger.info(f"Now playing - {elem.name}\n{elem.path}\n{Queue.getSTR()}")


def onEndOfSong(elem, Queue):
    logger.info(f"Ended - {elem.name}\n{Queue.getSTR()}")


def onAdditionToTheQueue(Queue):
    logger.info(f"Song is added to the queue, but not played yet\nQueue:\n{Queue.getSTR()}")


def onDownloadOfTrack(filename):
    logger.info(f'Downloaded file - {filename}')


def onEndOfQueue():
    logger.info("Queue ended")


def onReceiveOfTrack(name, reps):
    logger.info(f'Received to play "{name}", {reps+ 1} times')


def onSkip():
    logger.info("Skipped track...")


def onStop():
    logger.info("Stopped playing tracks...")

# add to embed
def queueMessage(songQueue):
    embed = discord.Embed(colour=discord.Colour.random(), title="Очередь пуста")
    if songQueue:
        content, embed = songQueue.get(), discord.Embed(colour=discord.Colour.random(), title="Очередь:")
        for song in content[:10]:
            embed.add_field(name=f'{song["pos"]}.', value=f"{song['name']} ({song['dur']})")
    return embed


def onPause():
    logger.info("Paused song.")


async def onUnpause():
    logger.info("Resumed song.")


async def onEndlessON(message, Queue, mode):
    currSong = Queue[0]
    if mode:
        await message.reply(f"{currSong.name} будет проигрываться бесконечно.")
        logger.info(f"Endless song - ON: {currSong.name}")
    else:
        await message.reply(f"{currSong.name} не будет проигрываться бесконечно.")
        logger.info(f"Endless song - OFF: {currSong.name}")


def onClientAutoplay(mode):
    if mode:
        logger.info(f"Received autoplay")
    else:
        logger.info(f"Autoplay - OFF")


async def onEndOfQueueButAutoplayIsOn(songQueue):
    logger.info(f"Queue is ended, but because autoplay is on, queue continues.")


def onRawResponse(response):
    if response:
        logger.info(f"GPT response:\n{response}")
    else:
        logger.info(f"GPT is shit")


async def onJoinToVoice(voice_client):
    directory = f"ffmpeg/audioMessages/OnJoin/{choice(os.listdir('ffmpeg/audioMessages/OnJoin'))}"
    file = (discord.FFmpegPCMAudio(executable=ffmpegEXEpath, source=directory))
    voice_client.play(file)
    await asyncio.sleep(5)


async def onLeave(voice_client):
    directory = f"ffmpeg/audioMessages/OnLeave/{choice(os.listdir('ffmpeg/audioMessages/OnLeave'))}"
    file = (discord.FFmpegPCMAudio(executable=ffmpegEXEpath, source=directory))
    voice_client.play(file)
    await asyncio.sleep(5)
