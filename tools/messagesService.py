import asyncio

import discord
import logging
import platform
import os
import tools.tools as computations
from tools.info import ffmpegEXEpath
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


async def onCurrSong(msg, elem):
    embed = discord.Embed(
        url=elem.url,
        title=f"Сейчас играет - {elem.name}",
        description=f"{elem.duration // 60}:{str(elem.duration % 60).rjust(2, '0')}",
        colour=discord.Colour.random(),
    )
    embed.set_image(url=computations.getThumbnailUrl(elem.url))
    await msg.channel.send(embed=embed)


def onNowPlaying(elem, Queue):
    logger.info(f"Now playing - {elem.name}\n{elem.path}\n{Queue.getSTR()}")


def onEndOfSong(elem, Queue):
    logger.info(f"Ended - {elem.name}\n{Queue.getSTR()}")


def onAdditionToTheQueue(Queue):
    logger.info(f"Song is added to the queue, but not played yet\nQueue:\n{Queue.getSTR()}")
    return


def onDownloadOfTrack(filename):
    logger.info(f'Downloaded file - {filename}')


def onEndOfQueue():
    logger.info("Queue ended")


def onReceiveOfTrack(name, reps):
    logger.info(f'Received to play "{name}", {reps+ 1} times')


async def onSkip(message):
    await message.reply(f"Пропустил песню.")
    logger.info("Skipped track...")


async def onStop(message):
    await message.channel.send(f"ББ")
    logger.info("Stopped playing tracks...")


def queueMessage(songQueue):
    embed = discord.Embed(colour=discord.Colour.random(), title="Очередь пуста")
    if songQueue:
        content, embed = songQueue.get(), discord.Embed(colour=discord.Colour.random(), title="Очередь:")
        for song in content[:10]:
            embed.add_field(name=f'{song["pos"]}.', value=f"{song['name']} ({song['dur']})")
    return embed


async def onPause(message):
    await message.reply(f"Поcтавил на паузу")
    logger.info("Paused song.")


async def onUnpause(message):
    await message.reply(f"Продолжаю проигрывание")
    logger.info("Resumed song.")


async def onEndlessON(message, Queue, mode):
    currSong = Queue[0]
    if mode:
        await message.reply(f"{currSong.name} будет проигрываться бесконечно.")
        logger.info(f"Endless song - ON: {currSong.name}")
    else:
        await message.reply(f"{currSong.name} не будет проигрываться бесконечно.")
        logger.info(f"Endless song - OFF: {currSong.name}")


async def onClientAutoplay(message: discord.Message, mode):
    if mode:
        logger.info(f"Received autoplay")
    else:
        logger.info(f"Autoplay - OFF")


async def onEndOfQueueButAutoplayIsOn(message: discord.Message, songQueue):
    logger.info(f"Queue is ended, but because autoplay is on, queue continues.")

    content, embed = songQueue.get(), discord.Embed(
        colour=discord.Colour.random(),
        title="Очередь:",
        description="Так как включено автопроигрывание, очередь продолжается"
    )
    for song in content[:10]:
        embed.add_field(name=f'{song["pos"]}.', value=f"{song['name']} ({song['dur']})")

    # await message.channel.send()


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
