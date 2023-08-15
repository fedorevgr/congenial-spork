import logging
import discord.ext.commands as ds
import discord
from tools.info import TOKEN, DeveloperDiscordId
import tools.tools as computations
import ffmpeg.player as player
from database.Interfaces import queue
from ffmpeg.audioManager import clearCache
import tools.messagesService as systemMessages

logger = logging.getLogger("discord")
bot = ds.Bot(owner_id=DeveloperDiscordId, command_prefix="~", intents=discord.Intents.all())
db = None
voiceClient: discord.VoiceClient
songQueue = queue.Interface()


@bot.event
async def on_ready():
    systemMessages.logOnStartUp(bot.user.name)
    clearCache()


@bot.command()
async def join(message:  discord.Message):
    global voiceClient
    voiceClient = await message.author.voice.channel.connect()


@bot.command()
async def play(message: discord.Message, *args: str):
    global voiceClient
    global songQueue
    global logger
    async with message.channel.typing():
        songName, repeat = computations.assignNameReps(args)
        logger.info(f'Received to play "{songName}", {repeat+1} times')

        if not bot.voice_clients:
            await join(message)

    await player.play(
        urloname=songName,  client=bot, voice_client=voiceClient, Queue=songQueue, msg=message, repeat=repeat
    )


@bot.command()
async def stop(message):
    global voiceClient
    voiceClient.stop()
    logger.info("Stopped playing tracks...")
    await voiceClient.disconnect()


@bot.command()
async def skip(message):
    global voiceClient
    voiceClient.stop()
    logger.info("Skipped track...")


@bot.command()
async def queue(message: discord.Message):
    global songQueue
    embed = discord.Embed(colour=discord.Colour.random(), title="Очередь пуста")
    if songQueue:
        content, embed = songQueue.get(), discord.Embed(colour=discord.Colour.random(), title="Очередь:")
        for song in content[:10]:
            embed.add_field(name=f'{song["pos"]}.', value=f"{song['name']} ({song['dur']})")
    await message.channel.send(embed=embed)


@bot.command()
async def pause(message):
    voiceClient.pause()
    player.changePause()


#@bot.event
#async def on_message(msg: discord.Message):
#    await msg.delete(delay=1)



bot.run(token=TOKEN, reconnect=True)

