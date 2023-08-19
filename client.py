import asyncio

import discord.ext.commands as ds
import discord
from tools.info import DeveloperDiscordId
import tools.tools as computations
import ffmpeg.player as player
from database.Interfaces import queue
from ffmpeg.audioManager import clearCache
import tools.messagesService as systemMessages


TOKEN = open("TOKEN.txt", "r").read()
bot = ds.Bot(owner_id=DeveloperDiscordId, command_prefix="~", intents=discord.Intents.all())
db = None
voiceClient: discord.VoiceClient
songQueue = queue.Interface()


@bot.event
async def on_ready():
    systemMessages.logOnStartUp(bot.user.name)
    player.autoplay.setAutoplayMode(True)
    clearCache()


@bot.command()
async def join(message:  discord.Message):
    global voiceClient
    voiceClient = await message.author.voice.channel.connect()


@bot.command()
async def play(message: discord.Message, *args: str):
    global voiceClient
    global songQueue
    async with message.channel.typing():
        songName, repeat = computations.assignNameReps(args)
        systemMessages.onReceiveOfTrack(songName, repeat)

        if not bot.voice_clients:
            await join(message)
            await systemMessages.onJoinToVoice(voiceClient)

    await player.play(
        urloname=songName,  client=bot, voice_client=voiceClient, Queue=songQueue, msg=message, repeat=repeat
    )


@bot.command()
async def stop(message):
    global voiceClient
    global songQueue
    voiceClient.stop()

    songQueue.clear()
    player.autoplay.cleanUp()
    player.timer.cleanUp()

    await systemMessages.onLeave(voiceClient)
    await systemMessages.onStop(message)
    await voiceClient.disconnect()


@bot.command()
async def skip(message):
    global voiceClient
    voiceClient.pause()
    player.timer.switchSkip()
    await systemMessages.onSkip(message)


@bot.command()
async def queue(message: discord.Message):
    global songQueue
    await message.channel.send(embed=systemMessages.queueMessage(songQueue))


@bot.command()
async def pause(message: discord.Message):
    if player.timer.switchPause():
        voiceClient.pause()
        await systemMessages.onPause(message)
    else:
        voiceClient.resume()
        await systemMessages.onUnpause(message)


@bot.command()
async def endless(msg: discord.Message):
    global songQueue
    isSwitchedON = player.timer.switchEndless()
    await systemMessages.onEndlessON(msg, songQueue, isSwitchedON)


@bot.command()
async def autoplay(msg: discord.Message):
    global songQueue
    if not player.autoplay.getAutoplayMode():
        await systemMessages.onClientAutoplay(msg, mode=True)
        await player.autoplay.AutoplayToQueue(songQueue=songQueue, message=msg)
    else:
        await systemMessages.onClientAutoplay(msg, mode=False)
        player.autoplay.setAutoplayMode(mode=False)
        if songQueue:
            songQueue.leaveFirstSong()


bot.run(token=TOKEN, reconnect=True)

