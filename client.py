import asyncio
import datetime
import logging

import discord.ext.commands as ds
import discord
from TOOLS.info import DeveloperDiscordId
from discord.ext.commands.context import Context
import ffmpeg.player as player
from database.Interfaces import queue
from ffmpeg.audioManager import clearCache
import TOOLS.messagesService as systemMessages
from TOOLS import embeds
import TOOLS.tools as computations


TOKEN = open("TOKEN.txt", "r").read()
bot = ds.Bot(owner_id=DeveloperDiscordId, command_prefix="~", intents=discord.Intents.all())
db = None
voiceClient: discord.VoiceClient
songQueue = queue.Interface()
logger = logging.getLogger("discord")


@bot.event
async def on_ready():
    systemMessages.logOnStartUp(bot)
    player.autoplay.setAutoplayMode(False)
    c = await bot.tree.sync()

    clearCache()


async def join(message:  discord.Message):
    global voiceClient
    voiceClient = await message.author.voice.channel.connect()
    await systemMessages.onJoinToVoice(voiceClient)


@bot.hybrid_command()
async def stop(message):
    global voiceClient
    global songQueue
    voiceClient.stop()

    songQueue.clear()
    player.autoplay.cleanUp()
    player.timer.cleanUp()

    await message.replay("ББ")
    await systemMessages.onLeave(voiceClient)
    await systemMessages.onStop()
    await voiceClient.disconnect()


@bot.command()
async def skip(message):
    global voiceClient
    voiceClient.pause()
    player.timer.switchSkip()
    await systemMessages.onSkip()


@bot.command()
async def queue(message: discord.Message):
    global songQueue
    # change
    await message.channel.send(embed=systemMessages.queueMessage(songQueue))


@bot.command()
async def pause(message: discord.Message):
    if player.timer.switchPause():
        voiceClient.pause()
        await systemMessages.onPause()
    else:
        voiceClient.resume()
        await systemMessages.onUnpause()


@bot.command()
async def endless(msg: discord.Message):
    global songQueue
    isSwitchedON = player.timer.switchEndless()
    await systemMessages.onEndlessON(msg, songQueue, isSwitchedON)


@bot.command()
async def autoplay(msg: discord.Message):
    global songQueue
    if not player.autoplay.getAutoplayMode():
        systemMessages.onClientAutoplay(mode=True)
        await player.autoplay.AutoplayToQueue(songQueue=songQueue, message=msg)
    else:
        systemMessages.onClientAutoplay(mode=False)
        player.autoplay.setAutoplayMode(mode=False)
        if songQueue:
            songQueue.leaveFirstSong()


@bot.hybrid_command()
async def play(context: Context, track: str = "", repetitions: float = 0.0):
    global voiceClient
    global songQueue
    if track:
        if repetitions == float("inf"):
            isSwitchedON = player.timer.switchEndless()
        else:
            repetitions = int(repetitions) if repetitions >= 0 else -int(repetitions)

        #  reply to command  here due to issues
        name, url, duration = computations.assignNameUrlDuration(track)
        await context.reply(
            embed=embeds.ReceiveToQueue(songName=name, duration=duration, url=url)
        )

        if not bot.voice_clients:
            await join(message=context.message)

        await player.play(
            urloname=track,
            client=bot,
            voice_client=voiceClient,
            Queue=songQueue,
            context=context,
            repeat=repetitions
        )
    else:
        await context.reply(f"Да, играю я уже успокойся...")
        await player.playWithOutQueueAddition(
            voice_client=voiceClient,
            Queue=songQueue,
            msg=context.message
        )


@bot.hybrid_command()
async def test(context: discord.ext.commands.Context, data: str = ""):
    await context.reply(embed=embeds.TestEmbed())

bot.run(token=TOKEN, reconnect=True)

