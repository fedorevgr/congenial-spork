import discord
from ffmpeg import downloader
import logging
from youtubesearchpython import VideosSearch
from database.Interfaces import queue
import asyncio


logger = logging.getLogger("discord")


async def play(url, client: discord.Client, voice_client: discord.VoiceClient, Queue: queue.Interface, log):
    if not url.startswith("https"):
        name = url
        url = getUrl(url)
    else:
        name = getName(url)

    filename = await downloader.YTDLSource.from_url(url=url, loop=client.loop)
    # file downloaded put in queue

    await Queue.addSong(name=name, url=url, duration=getDuration(url), systemName=filename)

    logger.info(f'Downloaded file {filename}')

    if voice_client.is_playing():
        return

    for elem in Queue:
        filename = elem.path
        file = (discord.FFmpegPCMAudio(executable="ffmpeg/ffmpeg.exe", source=filename))
        voice_client.play(file)
        logger.info(f"Now playing {elem.name}")
        logger.info(Queue.get())
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        await Queue.skipSong()


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
    res = videoInfo["result"][0]['duration'].split(":")
    return 60*int(res[0]) + int(res[1])
