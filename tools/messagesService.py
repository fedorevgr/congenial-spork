import discord
import logging
import platform
import os
import tools.tools as computations


logger = logging.getLogger("discord")


def logOnStartUp(botName):
    logger.info(f"Logged in as {botName}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info(f"Working directory: "+ '/'.join(os.getcwd().split('\\')))
    logger.info("-------------------")


async def onAdditionOfSong(msg, name, elem):
    logger.info(f'Song "{name}" is added to queue.')
    message = f"Добавил die Musik -------  {name}  ({elem.duration // 60}:{str(elem.duration % 60).rjust(2, '0')})"
    await msg.reply(message)


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


async def onAutoplay(message, songToAutoplay, mode):
    if mode:
        await message.reply(f"{songToAutoplay.name} поставлена как на поток.")
        logger.info(f"{songToAutoplay.name} is now on autoplay\nAutoplay - ON")
    else:
        await message.reply(f"Поток по музыке остановлен")
        logger.info(f"\nAutoplay - OFF")

