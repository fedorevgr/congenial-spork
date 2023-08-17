import asyncio

import discord
from ffmpeg import downloader
from database.Interfaces import queue
import tools.tools as computations
import tools.messagesService as systemMessages
from ffmpeg.TimerService import Timer
from tools.info import ffmpegEXEpath
from ffmpeg.AutoplayService import AutoplayService


timer = Timer()
autoplay = AutoplayService()


async def play(
        urloname,
        client: discord.Client,
        voice_client: discord.VoiceClient,
        Queue: queue.Interface,
        msg: discord.Message,
        repeat=0
        ):

    global timer
    global autoplay

    async with msg.channel.typing():
        name, url = computations.assignNameUrl(urloname)

        filename = await downloader.YTDLSource.from_url(url=url, loop=client.loop)
        systemMessages.onDownloadOfTrack(filename)

        Queue.addSong(name=name, url=url, duration=computations.getDuration(url), systemName=filename, amount=repeat)

        await systemMessages.onAdditionOfSong(msg=msg,  name=name, elem=Queue[-1])

        if len(Queue) > 1 and len(Queue) - repeat > 1:
            return systemMessages.onAdditionToTheQueue(Queue)

    await _play(Queue=Queue, msg=msg, voice_client=voice_client)

    return


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
        Queue += preparedQueue[1:]
        await systemMessages.onEndOfQueueButAutoplayIsOn(message=msg, songQueue=Queue)

        await _play(Queue=Queue, msg=msg, voice_client=voice_client)
    systemMessages.onEndOfQueue()
    return
