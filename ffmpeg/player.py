import asyncio
import logging

import discord
from discord.ext.commands.context import Context
from ffmpeg import downloader
from database.Interfaces import queue
import tools.tools as computations
import tools.messagesService as systemMessages
from ffmpeg.TimerService import Timer
from tools.info import ffmpegEXEpath
from ffmpeg.AutoplayService import AutoplayService
from tools.embeds import *


timer = Timer()
autoplay = AutoplayService()
logger = logging.getLogger("discord")


async def play(
        urloname,
        client: discord.Client,
        voice_client: discord.VoiceClient,
        Queue: queue.Interface,
        context: Context,
        repeat=0
        ):

    global timer
    global autoplay

    async with context.channel.typing():
        name, url = computations.assignNameUrl(urloname)
        duration = computations.getDuration(url)

        filename = await downloader.YTDLSource.from_url(url=url, loop=client.loop)
        systemMessages.onDownloadOfTrack(filename)

        Queue.addSong(name=name, url=url, duration=duration, systemName=filename, amount=repeat)

        logger.info(f'Track "{name}", added to queue.')
        await context.reply(embed=ReceiveToQueue(songName=name, duration=duration, url=url))

        if len(Queue) > 1 and len(Queue) - repeat > 1:
            return systemMessages.onAdditionToTheQueue(Queue)

    await _play(Queue=Queue, msg=context.message, voice_client=voice_client)

    return


async def playWithOutQueueAddition(voice_client: discord.VoiceClient, msg: discord.Message, Queue: queue.Interface):
    await _play(Queue=Queue, voice_client=voice_client, msg=msg)


async def _play(Queue: queue.Interface, msg: discord.Message, voice_client):
    elem = Queue[0]
    while Queue:
        elem = Queue[0]
        systemMessages.onNowPlaying(elem, Queue)

        file = (discord.FFmpegPCMAudio(executable=ffmpegEXEpath, source=elem.path))
        voice_client.play(file)

        await systemMessages.onCurrSong(msg=msg, elem=elem)
        await timer.startTimer(elem.duration)

        if not timer.getEndless() and Queue:
            await Queue.skipSong()

        systemMessages.onEndOfSong(elem, Queue)

    if autoplay.getAutoplayMode():
        preparedQueue = await autoplay.AutoplayToQueue(queue.Interface([elem]))
        if preparedQueue:
            Queue += preparedQueue[1:]
            await systemMessages.onEndOfQueueButAutoplayIsOn(message=msg, songQueue=Queue)

            await _play(Queue=Queue, msg=msg, voice_client=voice_client)
    systemMessages.onEndOfQueue()
    return
