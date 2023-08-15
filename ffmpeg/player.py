import discord
from ffmpeg import downloader
import logging
from database.Interfaces import queue
import asyncio
import tools.tools as computations
import tools.messagesService as systemMessages
from ffmpeg.TimerService import Timer
from tools.info import ffmpegEXEpath


logger = logging.getLogger("discord")
timer = Timer()


async def play(
        urloname,
        client: discord.Client,
        voice_client: discord.VoiceClient,
        Queue: queue.Interface,
        msg: discord.Message,
        repeat=0
        ):
    global timer
    async with msg.channel.typing():
        name, url = computations.assignNameUrl(urloname)

        filename = await downloader.YTDLSource.from_url(url=url, loop=client.loop)
        # file downloaded put in queue
        logger.info(f'Downloaded file - {filename}')

        Queue.addSong(name=name, url=url, duration=computations.getDuration(url), systemName=filename, amount=repeat)

        await systemMessages.onAdditionOfSong(msg=msg,  name=name, elem=Queue[-1])

        if len(Queue) > 1 and len(Queue) - repeat > 1:
            logger.info(f"Song is added to the queue, but not played yet\nQueue:\n{Queue.getSTR()}")
            return

    while Queue:
        elem = Queue[0]

        logger.info(f"Now playing - {elem.name}\n{elem.path}\n{Queue.getSTR()}")

        file = (discord.FFmpegPCMAudio(executable=ffmpegEXEpath, source=elem.path))
        voice_client.play(file)

        await systemMessages.onCurrSong(msg=msg, elem=elem)

        await timer.startTimer(elem.duration)

        await Queue.skipSong()
        logger.info(f"Ended - {elem.name}\n{Queue.getSTR()}")

    logger.info("Queue ended")

