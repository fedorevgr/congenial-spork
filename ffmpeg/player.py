import discord
from ffmpeg import downloader
import logging
from youtubesearchpython import VideosSearch
from database.Interfaces import queue
import asyncio
from time import time


logger = logging.getLogger("discord")


async def play(
        url,
        client: discord.Client,
        voice_client: discord.VoiceClient,
        Queue: queue.Interface,
        repeat=0
        ):
    if not url.startswith("https"):
        name = url
        url, name = getUrl(url), getName(url)
    else:
        name = getName(url)

    filename = await downloader.YTDLSource.from_url(url=url, loop=client.loop)
    # file downloaded put in queue
    logger.info(f'Downloaded file - {filename}')

    for _ in range(repeat+1):
        await Queue.addSong(name=name, url=url, duration=getDuration(url), systemName=filename)

    logger.info(f'Song "{name}" is added to queue.')

    if Queue.qsize() != 0:
        logger.info(f"Song is added to the queue, but not played yet\nQueue:\n{Queue.get()}")
        return

    while Queue:
        elem = Queue.get()
        logger.info(f"Now playing - {elem.name}\n{elem.path}\n{Queue.get()}")
        filename = elem.path
        file = (discord.FFmpegPCMAudio(executable="ffmpeg/ffmpeg.exe", source=filename))
        voice_client.play(file)

        while True:
            await asyncio.sleep(1)
            if not voice_client.is_playing():
                break
        logger.info(f"Ended - {elem.name}\n{Queue.getInfo()}")

    logger.info("Queue ended")


def getUrl(fromName: str):
    videosSearch = VideosSearch(fromName, limit=1)
    video_info = videosSearch.result()
    video_url = video_info['result'][0]['link']
    return video_url


def getName(fromUrl):
    videoSearch = VideosSearch(fromUrl, limit=1)
    videoInfo = videoSearch.result()
    return videoInfo["result"][0]["title"]


def getDuration(fromUrl):
    videoSearch = VideosSearch(fromUrl, limit=1)
    videoInfo = videoSearch.result()
    res = videoInfo["result"][0]['duration'].split(":")[::-1]
    return sum([(60**i)*int(value) for i, value in enumerate(res)])
